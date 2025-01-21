from django.urls import path
from .views import CreateFolderAPI, FolderListAPI


urlpatterns = [
    path('folders/create/', CreateFolderAPI.as_view(), name='create_folder'),
    path('folders/list/',FolderListAPI.as_view(), name='get_folder'),
]