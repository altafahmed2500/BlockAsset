from django.contrib import admin
from .models import UserProfile, UserConnection, Incident

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserConnection)
admin.site.register(Incident)
