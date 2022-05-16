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


def user_page(request, user_id, num_page=1):
    try:
        list_type = "User Profile"
        page_user = User.objects.get(pk=user_id)
    except:
        return render(request, "network/not_found.html")
    if request.method == "POST":  # Switching the Follow status
        pass
    else:   # Displaying the users profile
        paginator = get_posts(list_type, page_user)
        return render(request, "network/index.html", {
            "list_type": list_type,
            "n_followers": page_user.followers.count(),
            "page_user": page_user,
            "cur_page": paginator.page(num_page),
            "num_page": num_page,
            "page_range": paginator.page_range
        })


def index(request, num_page=1):
    list_type = "All Posts"
    page_user = None
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
