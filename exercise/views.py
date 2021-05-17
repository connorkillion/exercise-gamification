from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.urls import reverse
from .forms import ExerciseForm, PostForm
from .models import Exercise, Profile, City, Post
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, CityForm, CurrentLocationUpdateForm
from django.contrib.auth.models import User
from django.views.generic import TemplateView, RedirectView
import requests
from django.core.exceptions import PermissionDenied
from django_oso.auth import authorize
from django.db.models import Count, Avg
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
import datetime
from django.template import RequestContext


# Utilized tutorial found at https://www.youtube.com/watch?v=FdVuKt_iuSI to create user profiles model/to register
# users in the app database

# Source for navigation bar and base template
# https://www.selimatmaca.com/211-base-template/

def directions(request):
    if not request.user.is_authenticated:
        return render(request, 'exercise/notloggedin_directions.html')
    return render(request, 'exercise/directions.html')


def new_post(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    form = PostForm(request.POST or None)
    if request.method == 'POST':
        form = PostForm(request.POST)   
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return redirect(reverse('exercise:posts'))
        else:
            form = PostForm()
           
    context = {'form': form}
    return render(request, 'exercise/new_post.html', context)


def list_posts(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    posts = Post.objects.all().order_by('-created_at')[:]
    return render(request, 'exercise/posts.html', {'posts': posts, 'username': request.user})


def delete_post(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    post = Post.objects.get(pk=id)
    if request.method == "POST":
        post.delete()
        return HttpResponseRedirect(reverse('exercise:posts'))
    return render(request, 'exercise/delete_post.html')


def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    exercise = Exercise.objects.filter(profile=request.user.profile)
    total_points = exercise.aggregate(total_points=Sum('points'))

    # SAVING POINTS TO PROFILE OF USER
    model = Profile
    if list(total_points.values())[0] is None:
        model.workout_points = 0
    else:
        model.workout_points = list(total_points.values())[0]
    request.user.profile.save()
    request.user.profile.current_location = request.user.profile.current_location.capitalize()
    points = model.workout_points

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():  # and p_form.is_valid():
            u_form.save()
            # messages.success(request, f'Your account has been updated! You are now able to log in')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
        # 'form': form,
        'total_points': total_points,
        'points': points
    }
    return render(request, 'exercise/profile.html', context)


def edit_profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your account has been updated! You are now able to log in')
            return HttpResponseRedirect(reverse('exercise:profile'))
        else:
            print(u_form.errors)
    else:
        u_form = UserUpdateForm(instance=request.user)
    return render(request, 'exercise/editprofile.html', {'u_form': u_form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            note = 'Your account has been created! You are now able to log in'
            return redirect('login')
    else:
        form = UserRegisterForm()
        return render(request, 'exercise/register.html', {'form': form})


def badge_info(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    return render(request, 'exercise/badge_info.html')


def badges(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    exercise = Exercise.objects.filter(profile=request.user.profile)
    total_points = exercise.aggregate(total_points=Sum('points'))
    ordered_exercises = exercise.order_by('-exercise_date')
    streak = 0
    things = []
    today = timezone.now()
    for item in ordered_exercises:
        #prev_date = today.scheduled_at.date()
        #date = item.scheduled_at.date()
        item = item.exercise_date
        if item >= today - datetime.timedelta(days=1) and item < today:
            streak += 1
            things.append(item)
            today = item
        elif item == today:
            today = item
        else:
            break
    context = {'total_points': total_points, 'streak': streak, 'things': things}
    return render(request, 'exercise/badges.html', context)


# Title: How To Build a Weather App in Django <br>
# Author: Anthony Herbert <br>
# Date: 03/29/21 <br>
# URL: https://www.digitalocean.com/community/tutorials/how-to-build-a-weather-app-in-django <br>
def edit_location(request):
    weather_data = []
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=e1d3b12bb66e2fbb73a45268f086a35e'
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = CurrentLocationUpdateForm(request.POST, instance=request.user.profile)
        # form = CurrentLocationUpdateForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data['current_location'])
            city = form.cleaned_data['current_location']
            try:
                # city = request.user.profile.current_location
                city_weather = requests.get(url.format(city)).json()
                weather = {
                    'city': city,
                    'temperature': city_weather['main']['temp'],
                    'description': city_weather['weather'][0]['description'],
                    'icon': city_weather['weather'][0]['icon']
                }
                weather_data.append(weather)
                form.save()
                # city.save()
                request.user.profile.save()
                return HttpResponseRedirect(reverse('exercise:home'))
            except KeyError:
                # print('Enter a valid city')
                messages.error(request, 'Please enter a valid city name')
        else:
            print(form.errors)
    else:
        form = CurrentLocationUpdateForm(instance=request.user.profile)
    return render(request, 'exercise/editlocation.html', {'weather_data': weather_data, 'form': form})


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'exercise/notloggedin.html')
    city = request.user.profile.current_location.capitalize()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=e1d3b12bb66e2fbb73a45268f086a35e'
    city_weather = requests.get(url.format(city)).json()
    weather = {
        'city': city,
        'temperature': city_weather['main']['temp'],
        'description': city_weather['weather'][0]['description'],
        'icon': city_weather['weather'][0]['icon']
    }

    form = ExerciseForm()
    exercise = Exercise.objects.filter(profile=request.user.profile).order_by("-created_at")
    total_points = exercise.aggregate(total_points=Sum('points'))
    if len(exercise) != 0:
        exercise = exercise[0]
        exercise.exercise_date = exercise.exercise_date.strftime('%b %d')
    user_workouts = {
        'user_points' : total_points,
        'user_exercise' : exercise,
    }

    context = {
        'weather': weather,
        'user_workouts': user_workouts
    }
    return render(request, 'exercise/HomeLogin.html', context)


def my_ws(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    form = ExerciseForm()
    exercise = Exercise.objects.filter(profile=request.user.profile).order_by("-exercise_date")
    # print(exercise)
    total_points = exercise.aggregate(total_points=Sum('points'))
    Profile.workout_points = total_points
    args = {'form': form, 'exercise': exercise, 'total_points': total_points}
    return render(request, 'exercise/MyWorkouts.html', args)


def delete_workout(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    workout = Exercise.objects.get(pk=id)
    points = int(workout.points)
    total_points = 0
    exercise = Exercise.objects.filter(profile=request.user.profile).order_by("-exercise_date")
    for object in exercise:
        total_points = total_points + object.points
    if request.method == "POST":
        workout.delete()
        request.user.profile.workout_points = total_points - points
        request.user.profile.num_workouts = request.user.profile.num_workouts - 1
        request.user.profile.save()
        return HttpResponseRedirect(reverse('exercise:my_ws'))
    return render(request, 'exercise/delete_workout.html', {'total_points': request.user.profile.workout_points})


def log_nws(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/') 
    if request.method == 'POST':
        filled_form = ExerciseForm(request.POST)
        print(filled_form.errors)
        total = 0
        # model.points = 5
        # user_profile = Profile._meta.get_field('workout_points')
        if filled_form.is_valid():
            if filled_form.cleaned_data['exercise_date'] > timezone.now():
                print('Date cannot be in the future')
                messages.error(request, 'Please enter a date that is not in the future.')
            model = filled_form.save(commit=False)
            model.points = 5
            model.profile = Profile.objects.get(user=request.user)

            # model.exercise = Exercise.objects.get(exercise_type=request.user)
            if filled_form.cleaned_data['time_taken'] == 'Longer Workout (Between 30-59 min)':
                model.points*=2
            elif filled_form.cleaned_data['time_taken'] == 'Long Workout (Between 60 and 119 min)':
                model.points*=4
            elif filled_form.cleaned_data['time_taken'] == 'Very Long Workout (120 min or greater)':
                model.points*=8
            if filled_form.cleaned_data['exercise_type'] == 'Cardio':
                model.points*=2
            elif filled_form.cleaned_data['exercise_type'] == 'Strength':
                model.points*=3
            elif filled_form.cleaned_data['exercise_type'] == 'Sports':
                model.points*=4
            if filled_form.cleaned_data['location'] == 'Outdoors':
                model.points*=2

            # request.user.profile.workout_points += model.points
            request.user.profile.award_points(model.points)
            request.user.profile.num_workouts += 1
            # if request.user.profile.num_workouts > 0:
            #     request.user.profile.avg_points = request.user.profile.workout_points/request.user.profile.num_workouts
            # else:
            #     request.user.profile.avg_points = request.user.profile.workout_points
            request.user.profile.save()
            model.save()
            return HttpResponseRedirect(reverse('exercise:my_ws'))
        else:
            # print("Please enter a date that is not in the future")
            messages.error(request, 'Please enter a date that is not in the future.')

        new_form = ExerciseForm()
        return render(request, 'exercise/LogNW.html', {'exerciseform':new_form})
    else:
        form = ExerciseForm()
        return render(request, 'exercise/LogNW.html', {'exerciseform': form})


def leaderboard(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/') 
    all_users = User.objects.all()
    # leader_board = Profile.objects.order_by('-avg_points')[:]
    leader_board = Profile.objects.all()
    # avg_points = []
    for rank in leader_board:
        if rank.num_workouts > 0:
            rank.avg_points = rank.workout_points/rank.num_workouts
        else:
            rank.avg_points = rank.workout_points

        # request.user.profile.save()
        rank.save()
    leader_board_avg = Profile.objects.all().order_by('-avg_points')[:]
    # for r in leader_board_avg:
    #     print(r.avg_points)
    context = {
        'all_users': all_users,
        'leader_board': leader_board,
        # 'avg_points': avg_points,
        'leader_board_avg': leader_board_avg,
    }
    return render(request, 'exercise/leaderboard.html', context)

# Website used to help with issue with logging out user
# https://stackoverflow.com/questions/5315100/how-to-configure-where-to-redirect-after-a-log-out-in-django


def log_out(request):
    logout(request)
    return HttpResponseRedirect('')





# def index(request):
#     if not request.user.is_authenticated:
#         return render(request, 'exercise/notloggedin.html')
#     url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=e1d3b12bb66e2fbb73a45268f086a35e'
#     weather_data = []
#     # print(type(weather_data))
#     cities = City.objects.all()
#     # cities = City.objects.all().filter(profile=request.user.profile)
#     all_cities = City.objects.all()
#     print(all_cities)
#     # print(cities)
#     if request.method == 'POST':
#         form = CityForm(request.POST)
#         if form.is_valid():
#             form.save()
#     form = CityForm()
#
#     # form = ExerciseForm()
#     # exercise = Exercise.objects.filter(profile=request.user.profile).order_by("-exercise_date")
#     # total_points = exercise.aggregate(total_points=Sum('points'))
#     # Profile.workout_points = total_points
#     # args = {'form': form, 'exercise': exercise, 'total_points': total_points}
#     # return render(request, 'exercise/MyWorkouts.html', args)
#     # request the API data and convert the JSON to Python data types
#     try:
#         for city in reversed(cities):
#             city_weather = requests.get(url.format(city)).json()
#             weather = {
#                 'city': city.name,
#                 'temperature': city_weather['main']['temp'],
#                 'description': city_weather['weather'][0]['description'],
#                 'icon': city_weather['weather'][0]['icon']
#             }
#             weather_data.append(weather)
#
#     except ValueError:
#         print('Does not match a city')
#     except KeyError:
#         pass
#
#     context = {'weather_data': weather_data, 'form': form}
#     # print(cities)
#     return render(request, 'exercise/index.html', context)
