from django.urls import path
from .views import CreateFolderAPI, FolderListAPI, FolderDetailAPI


urlpatterns = [
    path('folders/create/', CreateFolderAPI.as_view(), name='create_folder'),
    path('folders/list/',FolderListAPI.as_view(), name='get_folder'),
    path('folders/list/<int:folder_id>/',FolderListAPI.as_view(), name='navigate_folder'),
    path('folders/<int:folder_id>/', FolderDetailAPI.as_view(), name='fodler_detail')
]