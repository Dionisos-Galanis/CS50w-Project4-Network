from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from sqlalchemy import null

from .forms import AddPostForm
from .models import Post, User, Like, Comment
from .utils import get_posts


def like_switch(request):
    if request.method == "POST": # It always should be POST
        data = request.POST
        liker = request.user
        try:
            cur_post = Post.objects.get(pk=int(data['post_id']))
        except:
            return JsonResponse({"error": f"Post not found!"}, status=400)
        
        if data["like_action"] == "Like":
            try:
                Like.objects.get(post=cur_post, user=liker)
                return JsonResponse({"error": f"Like already exists!"}, status=400)
            except:
                Like.objects.create(post=cur_post, user=liker)
                cur_post.n_likes += 1
                cur_post.save()

        elif data["like_action"] == "Unlike":
            try:
                Like.objects.filter(post=cur_post, user=liker).delete()
                cur_post.n_likes -= 1
                cur_post.save()
            except:
                return JsonResponse({"error": f"Like not found!"}, status=400)

        else:   #Something is wrong
            return JsonResponse({"error": "Wrong action!"}, status=400)

        n_likes = cur_post.post_likes.count()
        return JsonResponse({"result": "OK", "n_likes": n_likes}, status=200)
    else:   # Something is wrong
        return JsonResponse({"error": "Error!"}, status=400)


def follow_switch(request):
    if request.method == "POST": # It always should be POST
        data = request.POST
        try:
            follower = User.objects.get(pk=int(data['follower']))
            followed = User.objects.get(pk=int(data['followed']))
        except:
            return JsonResponse({"error": f"Follower={int(data['follower'])} or Followed={int(data['followed'])} not found!"}, status=400)
        if data["follow_action"] == "Follow":
            follower.follow.add(followed)
        elif data["follow_action"] == "Unfollow":
            follower.follow.remove(followed)
        else:   #Something is wrong
            return JsonResponse({"error": "Wrong action!"}, status=400)
        n_followers = followed.followers.count()
        return JsonResponse({"result": "OK", "n_followers": n_followers}, status=200)
    else:   # Something is wrong
        return JsonResponse({"error": "Error!"}, status=400)


def followed(request, num_page=1):
    list_type = "Followed"
    followed = request.user.follow.all()
    # Displaying the users profile
    paginator = get_posts(list_type, followed)
    return render(request, "network/index.html", {
        "list_type": list_type,
        "followed": followed,
        "cur_page": paginator.page(num_page),
        "num_page": num_page,
        "page_range": paginator.page_range
    })


def user_page(request, user_id, num_page=1):
    try:
        list_type = "User Profile"
        page_user = User.objects.get(pk=user_id)
    except:
        return render(request, "network/not_found.html")
    # Displaying the users profile
    paginator = get_posts(list_type, page_user)
    return render(request, "network/index.html", {
        "list_type": list_type,
        "n_followers": page_user.followers.count(),
        "n_follows": page_user.follow.count(),
        "page_user": page_user,
        "cur_page": paginator.page(num_page),
        "num_page": num_page,
        "page_range": paginator.page_range
    })


def index(request, num_page=1):
    list_type = "All Posts"
    if request.method == "POST":  # Adding a new post
        add_post_form = AddPostForm(request.POST)
        if add_post_form.is_valid():
            post = Post(text=add_post_form.cleaned_data["text"],
                    author=request.user
                    )
            post.save()
            paginator = get_posts(list_type)
            return render(request, "network/index.html", {
                "add_post_form": AddPostForm(),
                "list_type": list_type,
                "cur_page": paginator.page(num_page),
                "num_page": num_page,
                "page_range": paginator.page_range
            })
        else:
            paginator = get_posts(list_type)
            return render(request, "network/index.html", {
                "add_post_form": AddPostForm(request.POST),
                "list_type": list_type,
                "cur_page": paginator.page(num_page),
                "num_page": num_page,
                "page_range": paginator.page_range
            })
    else:  # Displaying posts
        paginator = get_posts(list_type)
        return render(request, "network/index.html", {
            "add_post_form": AddPostForm(),
            "list_type": list_type,
            "cur_page": paginator.page(num_page),
            "num_page": num_page,
            "page_range": paginator.page_range
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
