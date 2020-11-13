from django.shortcuts import render
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import New, Vote

from .serializers import *


class NewRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = New.objects.all()
    serializer_class = NewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, **kwargs):
        new = New.objects.filter(pk=self.kwargs['pk'], author=self.request.user)
        if new.exists():
            return self.update(request, **kwargs)
        else:
            raise ValidationError('Новость может изменять только его создатель')

    def delete(self, request, *args, **kwargs):
        new = New.objects.filter(pk=self.kwargs['pk'], author=self.request.user)
        if new.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Новость может удалить только его создатель')


class NewList(generics.ListCreateAPIView):
    queryset = New.objects.all()
    serializer_class = NewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        new = New.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, new=new)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('Вы уже голосовали за эту новость')
        serializer.save(voter=self.request.user, new=New.objects.get(pk=self.kwargs['pk']))

    def delete(self, requests, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('Вы не голосовали за эту новость ')


class CommentCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, new_id=self.kwargs['pk'])

    def get_queryset(self):
        user = self.request.user
        return Comment.objects.filter(new_id=self.kwargs['pk'])


class CommentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Comment.objects.all()

    def put(self, request, **kwargs):
        comment = Comment.objects.filter(author=request.user, id=self.kwargs['pk'])
        if comment:
            return self.update(request, **kwargs)
        else:
            raise ValidationError('Изменять коментарий может только его создатель')

    def delete(self, request, *args, **kwargs):
        comment = Comment.objects.filter(author=request.user, id=self.kwargs['pk'])
        if comment:
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Коментарий может удалить только его создатель')
