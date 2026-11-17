from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST


def register(request):
    # Already logged in? No need to sign up again.
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log them in straight away
            messages.success(request, f"Welcome {user.username}! Your account has been created.")
            return redirect("index")
        # Form invalid -> fall through and show the SAME form with its errors.
        # (Before, it redirected to login and the errors were lost, which is why
        # people felt they had to sign up again and again.)
    else:
        form = UserCreationForm()
    return render(request, "users/register.html", {"form": form})


@require_POST
def custom_logout(request):
    logout(request)
    return render(request, "users/logout.html")
