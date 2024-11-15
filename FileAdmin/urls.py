from django.urls import path
from .views import fileUploadUpdateData, getUserUploadFiles,updateMetadata

urlpatterns = [
    path('upload', fileUploadUpdateData, name="File_upload_update_data"),
    path('getFiles', getUserUploadFiles, name='getUserUploadFiles'),
    path('update',updateMetadata, name="updateMetadata"),
]