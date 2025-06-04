from django.urls import path
from .views import wearable_data_view

urlpatterns = [
    path('', wearable_data_view, name='wearable_data_view'),
]
