
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:num_page>", views.index),
    path("user/<int:user_id>/<int:num_page>", views.user_page, name="user_page"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
