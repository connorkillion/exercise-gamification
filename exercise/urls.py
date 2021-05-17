from django.urls import path
from . import views
# from .views import UserWorkoutListView
# from exercise.views import MainView, AwardBadgeView, RevokeBadgeView

app_name = 'exercise'
urlpatterns = [   
    path('', views.home, name='home'),
    path('LogNW/', views.log_nws, name='log_new'),
    path('MyWorkouts/', views.my_ws, name='my_ws'),
    # path('MyPoints/', views.my_points, name='my_points'),
    # path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    # path('badges/', views.badge_list, name='badges'),
    # path('badgesdetail/', views.badge_detail, name='badge_detail'),
    # path('weather/', views.the_weather, name='weather')
    # path('weather/', views.index, name='weather'),
    path('editprofile/', views.edit_profile, name='editprofile'),
    path('badges/', views.badges, name='badges'),
    path('badgeinfo/', views.badge_info, name='badge_info'),
    path('posts/', views.list_posts, name='posts'),
    path('newpost/', views.new_post, name='new_post'),
    path('<int:id>/deletepost/', views.delete_post, name='delete_post'),
    path('<int:id>/deleteworkout/', views.delete_workout, name='delete_workout'),
    path('directions/', views.directions, name='directions'),
    # path('newpost/', views.PostView.as_view(), name='new_post'),
    # path('user/<str:username>', UserWorkoutListView.as_view(), name='user-workouts')
    # path('login/', views.login, name='login'),
    # path('logout/', views.logout, name='logout'),
    # path('main/', MainView.as_view(), name='main'),
    # path('award-badge/<int:badge_id>/', AwardBadgeView.as_view(), name='award-badge'),
    # path('revoke-badge/<int:badge_id>', RevokeBadgeView.as_view(), name='revoke-badge')
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('editlocation/', views.edit_location, name='editlocation'),
    path('notloggeddirections/', views.directions, name='notloggeddir'),

]

