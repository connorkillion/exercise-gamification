from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from .models import Exercise, Profile
import unittest

class ExerciseModelSetPointMethodTests(TestCase):
    def test_default(self):
        ex_obj = Exercise()
        ex_obj.set_points()
        self.assertEqual(ex_obj.points, 20)
    def test_second_branch(self):
        ex_obj = Exercise(time_taken='LESS_THAN_1_HR')
        ex_obj.set_points()
        self.assertEqual(ex_obj.points, 10)
    def test_third_branch(self):
        ex_obj = Exercise(time_taken='BETWEEN_1_AND_2_HRS')
        ex_obj.set_points()
        self.assertEqual(ex_obj.points, 15)
    def test_else_branch(self):
        ex_obj = Exercise(time_taken='MORE_THAN_2_HRS')
        ex_obj.set_points()
        self.assertEqual(ex_obj.points, 20)

## The following Django documentation, accessible through the below url, was used to help write the code in this test class.
## Title: Testing Tools
## Author: Django Documentation
## Date: 04/29/21
## URL: https://docs.djangoproject.com/en/3.1/topics/testing/tools/
## Test class ensures that all URL paths are correctly functioning when a user is not logged in; non-logged in users will not be able to url hop through our application. 
class WorkingURLPathsNotLoggedIn(TestCase):
    def test_home_page(self):
        response = self.client.get('/', follow=True)
        self.assertContains(response, "Login with Google", status_code=200) 
    def test_admin_page(self):
        response = self.client.get('/admin/', follow=True)
        self.assertContains(response, "Username:", status_code=200) 
    def test_profile_page(self):
        response = self.client.get('/profile/', follow=True)
        self.assertContains(response, "Login with Google", status_code=200) 
    def test_login_page(self):
        response = self.client.get('/login/', follow=True)
        self.assertContains(response, "Login with Google", status_code=200) 
    def test_logout_page(self):
        response = self.client.get('/logout/', follow=True)
        self.assertContains(response, "Login with Google", status_code=200) 
    def test_logNW_page(self):
        response = self.client.get('/LogNW/', follow=True)
        self.assertContains(response, "Login with Google", status_code=200) 
    def test_my_workouts_page(self):
        response = self.client.get('/MyWorkouts/', follow=True)
        self.assertContains(response, "Login with Google", status_code=200) 
    def test_edit_profile_page(self):
        response = self.client.get('/editprofile/', follow=True)
        self.assertContains(response, "Login with Google", status_code=200) 
    def test_badges_page(self):
        response = self.client.get('/badges/', follow=True)
        self.assertContains(response, "Login with Google", status_code=200) 
    def test_posts_page(self):
        response = self.client.get('/posts/', follow=True)
        self.assertContains(response, "Login with Google", status_code=200) 
    def test_newpost_page(self):
        response = self.client.get('/newpost/', follow=True)
        self.assertContains(response, "Login with Google", status_code=200) 
    def test_directions_page(self):
        response = self.client.get('/directions/', follow=True)
        self.assertContains(response, "HOW TO USE THE APP", status_code=200) 
    def test_leaderboard_page(self):
        response = self.client.get('/leaderboard/', follow=True)
        self.assertContains(response, "Login with Google", status_code=200) 
    def test_edit_location_page(self):
        response = self.client.get('/editlocation/', follow=True)
        self.assertContains(response, "Login with Google", status_code=200) 
    def test_not_logged_directions_page(self):
        response = self.client.get('/notloggeddirections/', follow=True)
        self.assertContains(response, "HOW TO USE THE APP", status_code=200) 

## Test class ensures that all URL paths are correctly functioning when a user is logged in;
class WorkingURLPathsLoggedIn(TestCase):
    ## I would not been able to write this test class without the help of this stackoverflow answer provided by Vladir Parrado Cruz;
    ## this answer was crucial in allowing me to create a superuser in the setUp method for this class 
    ## Title: Test Login with credentials as superuser Django 1.9, Python 3.5 
    ## Author: Vladir Parrado Cruz 
    ## Date: 04/29/21 
    ## URL: https://stackoverflow.com/questions/36163367/test-login-with-credentials-as-superuser-django-1-9-python-3-5
    def setUp(self): 
        self.client = Client()
        self.my_admin = User(username='tester', is_staff=True)
        self.my_admin.set_password('password')
        self.my_admin.save()
        response = self.client.get('/admin/', follow=True)
        loginresponse = self.client.login(username='tester',password='password')
        self.assertTrue(loginresponse) ## ensure that the superuser has succesfully logged in 
    def test_logged_in_home_page(self):
        response = self.client.get('/', follow=True)
        self.assertContains(response, "The current weather", status_code=200) 
    def test_logged_in_directions_page(self):
        response = self.client.get('/directions/', follow=True)
        self.assertContains(response, "Workouts", status_code=200) 
    def test_logged_in_profile_page(self):
        response = self.client.get('/profile/', follow=True)
        self.assertContains(response, "Username: ", status_code=200) 
    def test_logged_in_edit_profile_page(self):
        response = self.client.get('/editprofile/', follow=True)
        self.assertContains(response, "Update", status_code=200) 
    def test_logged_in_edit_location_page(self):
        response = self.client.get('/editlocation/', follow=True)
        self.assertContains(response, "Current location", status_code=200) 
    def test_logged_in_newpost_page(self):
        response = self.client.get('/newpost/', follow=True)
        self.assertContains(response, "Post any tips, tricks, or accomplishments you would like to share with the community!", status_code=200) 
    def test_logged_in_posts_page(self):
        response = self.client.get('/posts/', follow=True)
        self.assertContains(response, "Learn about tips and tricks to lead a healthier lifestyle from other users!", status_code=200) 
    def test_logged_in_logNW_page(self):
        response = self.client.get('/LogNW/', follow=True)
        self.assertContains(response, "Log and View All Workouts", status_code=200) 
    def test_logged_in_my_workouts_page(self):
        response = self.client.get('/MyWorkouts/', follow=True)
        self.assertContains(response, "Here you can see all your workouts!", status_code=200) 
    def test_logged_in_badge_info_page(self):
        response = self.client.get('/badgeinfo/', follow=True)
        self.assertContains(response, "Get points by logging your workouts!", status_code=200) 
    def test_logged_in_badges_page(self):
        response = self.client.get('/badges/', follow=True)
        self.assertContains(response, "Share My Accomplishments!", status_code=200)
    def test_logged_in_leaderboard_page(self):
        response = self.client.get('/leaderboard/', follow=True)
        self.assertContains(response, "See where you are in the rankings!", status_code=200) 