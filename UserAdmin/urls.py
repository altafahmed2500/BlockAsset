from django.urls import path
from .views import create_user_profile,get_all_user_profiles,secure_view,login_view,logout_view


urlpatterns = [
    path('register', create_user_profile, name='create_user_profile'),
    path('login', login_view, name='login_view'),
    path('logout', logout_view, name='logout_view'),
    path('all-users', get_all_user_profiles, name='get_all_user_profiles'),
    path('secure', secure_view, name='secure_view'),
]