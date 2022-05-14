from .models import Post, User, Like, Comment


def get_posts(list_type, page, page_user=None):
    if (list_type == "All Posts"):
            posts = Post.objects.order_by("-date_time")
    elif (list_type == "User Profile"):
            posts = Post.objects.filter(author=page_user).order_by("-date_time")

    # paginator = Paginator(posts, 10)
    return posts