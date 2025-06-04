from django.urls import path
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .views import test_contract, admin_ether_push, admin_ether_balance, admin_ether_push_allusers

urlpatterns = [
    path('testContract', test_contract, name='test_contract'),
    path('pushEther', login_required(require_POST(admin_ether_push)), name='admin_ether_push'),
    path('accountBalance', login_required(admin_ether_balance), name='admin_ether_balance'),
    path('pushEtherToall', login_required(require_POST(admin_ether_push_allusers)), name='admin_ether_push_allusers'),
]