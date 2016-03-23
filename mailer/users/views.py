from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate
from django.contrib.auth import login as auth_login
from django.core.urlresolvers import reverse

from mailer.users.forms import RegisterForm, LoginForm


# Create your views here.
def sign_up(request):
    request.session.flush()
    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            data = form.cleaned_data
            user = authenticate(
                email=data['email'], password=data['password'])

            if user is not None and user.is_active:
                auth_login(request, user)
                return redirect("/")

    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


def login(request):
    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                email=data['email'], password=data['password'])

            if user is not None:
                auth_login(request, user)
                return redirect("/")
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect(reverse("home"))

