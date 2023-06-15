from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from main.models import Profile
from main.utils import *


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

    return render(request, 'login.html', context={"error": error, "email": email})


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
    if request.method == 'POST':
        age = int(request.POST['age'])
        gender = request.POST['gender']
        height = int(request.POST['height'])
        weight = int(request.POST['weight'])
        activity_level = request.POST['activity_level']
        goal = request.POST['goal']
        utilisateur = Profile.objects.get(user=request.user)
        utilisateur.age = age
        utilisateur.goal = goal
        utilisateur.height = height
        utilisateur.weight = weight
        utilisateur.gender = gender
        utilisateur.activity_level = activity_level
        utilisateur.save()
        return redirect(profile)

    return render(request, 'survey.html', context={})


@login_required(login_url="login")
def profile(request):
    user = Profile.objects.get(user=request.user)
    # if profile incomplete
    if all(field is None for field in [user.age,user.gender,user.height,user.weight,user.activity_level]):
        redirect(survey)
    workout_plan = get_workout_recommendation(user.gender, user.age, user.height, user.weight, user.activity_level,
                                              user.goal)
    workout = [{"title": day[0], "exercices": list(map(lambda x: x.replace("li>", "").replace("</l",""), day[1]))} for day in workout_plan]
    benchmarked_bmi = calculateBenchmarkedBMI(user.age, user.gender)
    bmi = calculate_bmi(user.weight, user.height)
    diff_in_bmi = bmi - benchmarked_bmi
    if (diff_in_bmi > 0):
        bmi_rec = 'Based on Your BMI, we suggest you take up goals that help you reduce weight to reach your ideal BMI'
    elif (diff_in_bmi < 0):
        bmi_rec = 'Based on Your BMI, we suggest you take up goals that help you gain weight to reach your ideal BMI'
    else:
        bmi_rec = "Based on Your BMI, we suggest you take up goals that help you maintain weight to stay at your ideal BMI"
    calorie_intake = calculate_daily_calorie(user.age, user.gender, user.weight, user.height, user.activity_level,
                                             user.goal)
    recipe = recommend_recipes(calorie_intake['carbs'], calorie_intake['fat'], calorie_intake['protein'])

    schedule = []
    for i in range(0, 7):
        schedule.append(
            {
                "day": i+1,
                "workout": workout[i],
                "recipe": recipe[i],
            }
        )

    return render(request, "profile.html", context={'user': user, "schedule": schedule, "bmi": bmi, "bmi_rec": bmi_rec,
                                                    "calorie_intake": calorie_intake, })
