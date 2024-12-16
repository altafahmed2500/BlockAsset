from django.urls import path
from .views import test_contract, admin_ether_push, admin_ether_balance, admin_ether_push_allusers

urlpatterns = [
    path('testContract', test_contract, name='test_contract'),
    path('pushEther', admin_ether_push, name='admin_ether_push'),
    path('accountBalance', admin_ether_balance, name='admin_ether_balance'),
    path('pushEtherToall', admin_ether_push_allusers, name='admin_ether_push_allusers'),
]
