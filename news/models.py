from django.db import models
from django.contrib.auth.models import User


class New(models.Model):
    title = models.CharField(max_length=255, verbose_name='Описание')
    link = models.URLField(max_length=127, unique=True, verbose_name='Url')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    author = models.ForeignKey(User, max_length=127, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    new = models.ForeignKey(New, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']


class Vote(models.Model):
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    new = models.ForeignKey(New, on_delete=models.CASCADE)
