from .models import Post, User, Like, Comment
from django.core.paginator import Paginator


def get_posts(list_type, page_user=None):
    if (list_type == "All Posts"):
            posts = Post.objects.order_by("-date_time")
    elif (list_type == "User Profile"):
            posts = Post.objects.filter(author=page_user).order_by("-date_time")

    return Paginator(posts, 10)