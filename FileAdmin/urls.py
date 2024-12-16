from django.urls import path
from .views import fileUploadUpdateData, getUserUploadFiles, updateMetadata, uploadFileIPFS, get_user_files, \
    update_metadata_and_upload

urlpatterns = [
    path('upload', fileUploadUpdateData, name="File_upload_update_data"),
    path('getFiles', getUserUploadFiles, name='getUserUploadFiles'),
    path('update', updateMetadata, name="updateMetadata"),
    path('ipfsUpload', uploadFileIPFS, name="uploadFileIPFS"),
    path('getUserFiles', get_user_files, name="getUserFiles"),
    path('ipfsupload', update_metadata_and_upload, name="update_metadata_and_upload")
]
