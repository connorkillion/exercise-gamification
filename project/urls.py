from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from exercise import views as exercise_views

app_name = 'exercise'
urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('', include('exercise.urls')),
    path('admin/', admin.site.urls),
    # path('register/', exercise_views.register, name='register'),
    path('profile/', exercise_views.profile, name='profile'),
    path('login/', exercise_views.home),
    # path('login/', auth_views.LoginView.as_view(template_name='exercise/login.html'), name='login'),
    # path('logout/', auth_views.LoginView.as_view(template_name='exercise/logout.html'), name='logout'),
    path('logout/', auth_views.LogoutView.as_view(template_name='exercise/logout.html'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
