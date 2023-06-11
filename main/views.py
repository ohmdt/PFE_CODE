from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from main.models import Profile


def index(request):
    return render(request, "index.html", context={})


def loginView(request):
    error = None
    email = None
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        if email and password:
            if User.objects.filter(email=email).first():
                user = authenticate(username=email, password=password)
                print(user)
                if user:
                    login(request, user)
                    return redirect(survey)
                else:
                    error = "wrong Password"
            else:
                error = "user with this email doesn't exist!"
        else:
            error = "email and password are required! "

    return render(request, 'login.html', context={"error": error, "email":email})


def signup(request):
    error = None
    if request.user.is_authenticated:
        return redirect(survey)
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        age = request.POST.get('age', None)
        if User.objects.filter(email=email).first():

            error = 'User with the same email already exists'
        else:
            user = User.objects.create_user(email=email, username=email, password=password, first_name=first_name,
                                       last_name=last_name)
            profile = Profile.objects.create(user=user, age=age)
            login(request, user)
            return redirect(survey)
    return render(request, 'signup.html', context={'error': error})


@login_required(login_url="login")
def survey(request):
    return render(request, 'survey.html', context={})


@login_required(login_url="login")
def profile(request):
    utilisateur = Profile.objects.get(user=request.user)
    return render(request, "profile.html", context={'utilisateur':utilisateur})




