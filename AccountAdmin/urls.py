from django.urls import path

from .views import get_all_users, get_user_account

urlpatterns = [
    path('allUsers', get_all_users, name='get_all_users'),
    path('getAccountDetails', get_user_account, name='get_user_account'),
]
