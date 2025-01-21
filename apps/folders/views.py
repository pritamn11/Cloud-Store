from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Folder
from rest_framework.response import Response
from rest_framework import status
from .serializers import FolderSerializer
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
    serializer_class = FolderSerializer
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
