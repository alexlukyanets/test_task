from rest_framework import serializers
from .models import New, Vote, Comment
import json

class NewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_id = serializers.ReadOnlyField(source='author.id')
    votes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = New
        fields = '__all__'

    def get_votes(self, new):
        return Vote.objects.filter(new=new).count()

    def get_comments(self, new, **kwargs):
        data = Comment.objects.filter(new_id=new.id).values('id', 'content', 'author__username', 'created_at')
        if data:
            return data
        else:
            return None


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_id = serializers.ReadOnlyField(source='author.id')
    new = serializers.ReadOnlyField(source='new_id')

    class Meta:
        model = Comment
        fields = '__all__'

