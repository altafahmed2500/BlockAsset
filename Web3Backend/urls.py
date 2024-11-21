from django.urls import path
from .views import test_contract

urlpatterns = [
    path('testContract', test_contract, name='test_contract'),
]