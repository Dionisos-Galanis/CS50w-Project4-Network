
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:num_page>", views.index),
    path("follwed/<int:num_page>", views.followed, name="followed"),
    path("user/<int:user_id>/<int:num_page>", views.user_page, name="user_page"),
    path("followswitch", views.follow_switch, name="follow_switch"),
    path("likeswitch", views.like_switch, name="like_switch"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
