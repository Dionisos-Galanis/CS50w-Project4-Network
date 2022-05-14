from tkinter import CASCADE
from unittest import TextTestResult
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    follow = models.ManyToManyField('User', related_name='followers', blank=True)


class Post(models.Model):
    text = models.TextField()
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name="my_posts")
    date_time = models.DateTimeField(auto_now_add=True)
    n_likes = models.IntegerField(validators=[MinValueValidator(0)], default=0)


class Like(models.Model):
    user = models.ForeignKey('User', related_name='my_likes', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='post_likes', on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey('User', related_name='my_comments', on_delete=models.CASCADE)
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)