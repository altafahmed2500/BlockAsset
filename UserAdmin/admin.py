from django.contrib import admin
from .models import UserProfile, UserConnection

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserConnection)
