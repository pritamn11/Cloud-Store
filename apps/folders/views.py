from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Folder
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .serializers import FolderSerializer, ListFolderSerializer
from rest_framework import status
# Create your views here.

class CreateFolderAPI(APIView):
    serializer_class = FolderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request":request})
        if serializer.is_valid():
            # Save the folder and associate it with the authenticated user
            serializer.save(user=request.user)
            return Response({"message": "Folder created successfully!", "data": serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FolderListAPI(APIView):
    serializer_class = ListFolderSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        parent_folder_id = request.query_params.get("parent_folder")
        if parent_folder_id:
            folders = Folder.objects.filter(user=request.user, parent_folder_id=parent_folder_id)
        else:
            # Retrieve top-level folders if no parent_folder is specified
            folders = Folder.objects.filter(user=request.user, parent_folder__isnull=True)
        serializer = self.serializer_class(folders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FolderDetailAPI(APIView):
    serializer_class = ListFolderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, folder_id, user):
        """Retrieve folder by ID and ensure it belongs to the authenticated user."""
        try:
            return Folder.objects.get(id=folder_id, user=user)
        except Folder.DoesNotExist:
            return None
        
    def patch(self, request, folder_id):
        """Update folder name."""
        folder = self.get_object(folder_id, request.user)
        if not folder:
            return Response({"detail": "Folder not found or access denied."}, status=status.HTTP_404_NOT_FOUND)
        new_name = request.data.get("name")
        if not new_name:
            raise ValidationError({"detail": "Name field is required."})
        
        folder.name = new_name
        folder.save()
        return Response({"detail": "Folder name updated successfully."}, status=status.HTTP_200_OK)
    
    def delete(self, request, folder_id):
        """Delete folder and its subfolders."""
        folder = self.get_object(folder_id, request.user)
        if not folder:
            raise ValidationError({"detail": "Folder not found or access denied."})

        folder.delete()
        return Response({"detail": "Folder deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
