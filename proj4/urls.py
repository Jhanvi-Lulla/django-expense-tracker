from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    # Opening the plain website address now lands on the welcome page
    path("", RedirectView.as_view(pattern_name="welcome", permanent=False)),
    path("tracker/", include("tracker.urls")),
    path("register/", user_views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="users/login.html",
            redirect_authenticated_user=True,  # already logged in? skip the login page
        ),
        name="login",
    ),
    path("logout/", user_views.custom_logout, name="logout"),
]
