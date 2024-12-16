from django.urls import path

from .views import get_all_users, get_user_account, get_user_names_and_public_keys

urlpatterns = [
    path('allUsers', get_all_users, name='get_all_users'),
    path('getAddress', get_user_account, name='get_user_account'),
    path('userlist', get_user_names_and_public_keys, name="get_user_names_and_public_keys"),
]
