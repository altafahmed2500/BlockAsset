from django.urls import path
from .views import fileUploadUpdateData

urlpatterns = [
    path('upload', fileUploadUpdateData, name="File_upload_update_data"),
]