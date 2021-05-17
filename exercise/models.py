from django.db import models
from django.contrib.auth.models import User

from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.utils.timezone import now
import datetime
from datetime import timedelta
from django.utils import timezone
# from regex_field.fields import RegexField

# Source for 3rd party weather API
# https://www.digitalocean.com/community/tutorials/how-to-build-a-weather-app-in-django

# Source for Community posts feature
# https://www.osohq.com/post/building-django-app-with-data-access-control

# Image links
# https://img.pngio.com/bronze-medal-png-images-free-png-library-bronze-png-600_600.png
# https://i1.wp.com/wordsowers.com/wp-content/uploads/2017/01/silver-level1.png?fit=562%2C562
# https://th.bing.com/th/id/R84dfb027e4224af516af716f00ab61e3?rik=EEUBbK%2bGv%2b9afQ&riu=http%3a%2f%2fanimallawsource.
# org%2fwp-content%2fuploads%2f2015%2f08%2fgold-level.png&ehk=0IkwAb6rc%2fkDekvBKFYQP%2flI1PRyvvBxpFlmM8ntFAg%3d&risl=&pid=ImgRaw


from django.core.exceptions import ValidationError
import re


# Title: Validators <br>
# Author: Django Project <br>
# Date: 05/01/21 <br>
# URL: https://docs.djangoproject.com/en/3.2/ref/validators/ <br>
def validate_hash(value):
    reg = re.compile("^([a-zA-Z\u0080-\u024F]+(?:. |-| |'))*[a-zA-Z\u0080-\u024F]*$")
    if not reg.match(value):
        raise ValidationError(u'%s hashtag does not comply' % value)


# Title: Python Django Tutorial: Full-Featured Web App Part 8 - User Profile and Picture <br>
# Author: Corey Schafer <br>
# Date: 03/22/21 <br>
# URL: https://www.youtube.com/watch?v=FdVuKt_iuSI&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=8 <br>
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    workout_points = models.IntegerField(default=0)
    num_workouts = models.IntegerField(default=0)
    avg_points = models.IntegerField(default=0)
    current_location = models.CharField(max_length=50, default="Charlottesville")

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def award_points(self, workout_points):
        self.workout_points += workout_points
        self.save()


class Post(models.Model):
    # ACCESS_PUBLIC = 0
    # ACCESS_PRIVATE = 1
    # ACCESS_LEVEL_CHOICES = [
    #     (ACCESS_PUBLIC, 'Public'),
    #     (ACCESS_PRIVATE, 'Private'),
    # ]
    contents = models.TextField(max_length=180)
    # access_level = models.IntegerField(choices=ACCESS_LEVEL_CHOICES, default=ACCESS_PUBLIC)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class City(models.Model):
    # name = models.CharField(max_length=25)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'cities'
    profile = models.ForeignKey('Profile', null=True, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class InstagramAccount(models.Model):
    username = models.CharField(max_length=128)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username


class Publication(models.Model):
    picture = models.ImageField(upload_to="profile_pics")
    publish_at = models.DateTimeField()
    tags = models.ManyToManyField(Tag)
    instagram_account_id = models.ForeignKey(InstagramAccount, on_delete=models.CASCADE)

    def image_tag(self):
        return mark_safe("<img src='/%s' max-width='50' />" % self.picture)

    image_tag.short_description = "Picture"


class Exercise(models.Model):
    def __str__(self):
        return self.description

    """
    This method sets the points given a time taken (should probably modify later)
    """
    def set_points(self):
        ## self.points = int(self.time_taken) * 10
        if (self.time_taken == 'LESS_THAN_30'):
            self.points = 5
        elif (self.time_taken == 'LESS_THAN_1_HR'):
            self.points = 10
        elif (self.time_taken == 'BETWEEN_1_AND_2_HRS'):
            self.points = 15 
        else:
            self.points = 20 

    EXERCISE_CHOICES = [
        ('Cardio', 'Cardio'),
        ('Strength', 'Strength'),
        ('Sports', 'Sports'),
        ('Yoga/Flexibility', 'Yoga/Flexibility'),
    ]
    TIME_CHOICES = [
        ('Quick Workout (Between 1-29 min)', 'Quick Workout (Between 1-29 min)'),
        ('Longer Workout (Between 30-59 min)', 'Longer Workout (Between 30-59 min)'),
        ('Long Workout (Between 60 and 119 min)', 'Long Workout (Between 60 and 119 min)'),
        ('Very Long Workout (120 min or greater)', 'Very Long Workout (120 min or greater)'),
    ]
    LOCATION_CHOICES = [
        ('Indoors', 'Indoors'),
        ('Outdoors', 'Outdoors')
    ]

    # Title: Validators
    # Author: Django Project
    # Date: 05/01/21
    # URL: https://docs.djangoproject.com/en/3.2/ref/validators/

    def exclude_future_date(value):
        if value > timezone.now():
            raise ValidationError("The date cannot be in the future!")
        return value

    exercise_type = models.CharField(max_length=20, choices=EXERCISE_CHOICES, default='Cardio')
    location = models.CharField(max_length=8, choices=LOCATION_CHOICES, default='Indoors')
    exercise_date = models.DateTimeField('date completed', null=True, validators=[exclude_future_date])
    # time_taken = models.IntegerField(default=0)
    time_taken = models.CharField(max_length=100, choices=TIME_CHOICES, default='Quick Workout (Between 1-29 min)')
    points = models.IntegerField(default=0)
    description = models.CharField(max_length=200, blank=True)
    profile = models.ForeignKey('Profile', null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now, editable=False)
    # total_points = models.IntegerField(default=0)


