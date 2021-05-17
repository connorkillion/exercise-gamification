from django import forms 
from .models import Exercise, Profile, City, Post
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
# from regex_field.fields import RegexField
# from django.core.validations import RegexValidator

alphanumeric = RegexValidator(r'^[a-zA-Z]')


# Title: Regular Expressions for City Name <br>
#     Author: user2603432 <br>
# Date: 04/19/21 <br>
# URL: https://stackoverflow.com/questions/11757013/regular-expressions-for-city-name <br>
validator = RegexValidator(r"^([a-zA-Z\u0080-\u024F]+(?:. |-| |'))*[a-zA-Z\u0080-\u024F]*$", "The city shouldn't contain numbers" )


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = ['contents']
    
        widgets = {
            # 'contents': forms.TextInput(attrs={'class':'form-control','size': 1000,'placeholder': 'Write your tip/trick here.'}),
            'contents': forms.Textarea(attrs={'cols': 50, 'rows': 4, 'placeholder': 'Write your tip/trick/accomplishment here.'}),
        }


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'City Name'}),

        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    # email = forms.EmailField()

    ## https://stackoverflow.com/questions/34861322/override-maxlength-input-using-django-form-form-as-p 
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'maxlength': '12',
            'minlength': '4',
        })
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'maxlength': '12',
            'minlength': '2',
        })
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'maxlength': '12',
            'minlength': '2',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
    


class CurrentLocationUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['current_location']


# Title: Django 2.0 ModelForm dateField not displaying as a widget <br>
# Author: Gustavo Gradvohl <br>
# Date: 03/18/21
# URL: https://stackoverflow.com/questions/49440853/django-2-0-modelform-datefield-not-displaying-as-a-widget <br>
class ExerciseForm(forms.ModelForm):

    class Meta:
        LOCATION_CHOICES = [
            ('Indoors', 'Indoors'),
            ('Outdoors', 'Outdoors')
        ]
        model = Exercise
        exclude = ['points', 'profile']
        location = forms.ChoiceField(choices=LOCATION_CHOICES)

        widgets = {
            ## the following stack overflow post aided in writing the code for the exercise_date widget
            ## https://stackoverflow.com/questions/49440853/django-2-0-modelform-datefield-not-displaying-as-a-widget
            'exercise_date': forms.DateTimeInput(format=('%m/%d/%Y'),attrs={'class':'form-control','type':'date'}),
            # 'description': forms.TextInput(attrs={'class':'form-control','size': 50,'placeholder': 'Provide thoughts on your workout here.'}),
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 4, 'placeholder': 'Provide thoughts on your workout here.'}),
        }



