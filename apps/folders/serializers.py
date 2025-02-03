from rest_framework import serializers
from .models import Folder


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id', 'name', 'parent_folder', 'size', 'location', 'created_at', 'updated_at']
        read_only_fields = ['location', 'created_at', 'updated_at']
    
    def validate_parent_folder(self, value):
        """
        Validate that the parent folder belongs to the user.
        """
        user = self.context['request'].user
        if value and value.user != user:
            raise serializers.ValidationError("The parent folder does not belong to you.")
        return value
    

class ListFolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['name', 'parent_folder', 'size', 'location', 'created_at', 'updated_at']
        read_only_fields = ['location', 'created_at', 'updated_at']
    
    def validate_parent_folder(self, value):
        """
        Validate that the parent folder belongs to the user.
        """
        user = self.context['request'].user
        if value and value.user != user:
            raise serializers.ValidationError("The parent folder does not belong to you.")
        return value