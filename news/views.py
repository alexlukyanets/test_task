from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import New, Vote
from .serializers import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(request.POST['username'], password=request.POST['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except IntegrityError:
            return JsonResponse(({'error': 'That username has already been taken. Please choose a new username'}),
                                status=201)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return JsonResponse(({'error': 'Check username or password'}),
                                status=201)
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=200)


class NewListCreate(generics.ListCreateAPIView):
    queryset = New.objects.all()
    serializer_class = NewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = New.objects.all()
    serializer_class = NewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put_delete(self, method, request, error, **kwargs):
        new = New.objects.filter(pk=self.kwargs['pk'])
        if new:
            try:
                new.get(author=self.request.user)
                return method(request, **kwargs)
            except ObjectDoesNotExist:
                raise ValidationError(error)
        else:
            raise ValidationError('Такой новости не сущствует')

    def put(self, request, **kwargs):
        error = 'Новость может изменить только её создатель'
        return self.put_delete(self.update, request, error, **kwargs)

    def delete(self, request, *args, **kwargs):
        error = 'Новость может удалить только её создатель'
        return self.put_delete(self.destroy, request, error, **kwargs)


class CommentListCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            New.objects.get(pk=self.kwargs['pk'])
            serializer.save(author=self.request.user, new_id=self.kwargs['pk'])

        except ObjectDoesNotExist:
            raise ValidationError('Такой новости не существует')

    def get_queryset(self):
        new = New.objects.filter(pk=self.kwargs['pk'])
        if new.exists():
            comments = Comment.objects.filter(new_id=self.kwargs['pk'])
            if comments.exists():
                return comments
            else:
                return False
        else:
            return True

    def get(self, request, pk):
        queryset = self.get_queryset()
        if queryset == True:
            return Response({"Такой новости не существует"}, status=status.HTTP_204_NO_CONTENT)
        elif queryset == False:
            return Response({"Коментарии к этой новости пока отсутствуют"}, status=status.HTTP_204_NO_CONTENT)
        else:
            serializer = CommentSerializer(queryset, many=True).data
            return Response(serializer, status=status.HTTP_200_OK)


class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()

    def put_delete(self):
        comments = Comment.objects.filter(id=self.kwargs['pk'])
        if comments.exists():
            comment = Comment.objects.filter(author=self.request.user, id=self.kwargs['pk'])
            if comment.exists():
                return True
            else:
                return False
        else:
            raise ValidationError('Коментария с таким id существует')

    def put(self, request, **kwargs):
        if self.put_delete():
            return self.update(request, **kwargs)
        else:
            raise ValidationError('Изменять коментарий может только его создатель')

    def delete(self, request, *args, **kwargs):
        if self.put_delete():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Коментарий может удалить только его создатель')


class VoteCreateDestroy(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        new = New.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, new=new)

    def create_delete(self):
        user = self.request.user
        new = New.objects.filter(pk=self.kwargs['pk'])
        if new.exists():
            return Vote.objects.filter(voter=user, new=self.kwargs['pk'])
        else:
            raise ValidationError('Такой новости не существует')

    def perform_create(self, serializer):
        vote = self.create_delete()
        if vote != None:
            if not vote.exists():
                serializer.save(voter=self.request.user, new=New.objects.get(pk=self.kwargs['pk']))
                Response(status=status.HTTP_201_CREATED)
            else:
                raise ValidationError('Вы уже голосовали за эту новость')

    def delete(self, requests, *args, **kwargs):
        vote = self.create_delete()
        if vote != None:
            if vote:
                vote.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                raise ValidationError('Вы не голосовали за эту новость ')
