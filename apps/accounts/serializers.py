from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import ValidationError
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "avatar",
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        min_length=8, 
        max_length=30, 
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True, 
        min_length=8, 
        max_length=30, 
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'password2',
            "terms_agreement",
        ]
    
    def validate(self, attrs):
        """Validate passwords and terms agreement."""
        if attrs['password'] != attrs['password2']: 
            raise serializers.ValidationError(_("Password do not match."))
        
        if not attrs.get('terms_agreement', False):
            raise serializers.ValidationError(_("You must agree to the terms of service."))
        
        return attrs  
    
    def create(self, validated_data):
        """Create a new user instance."""
        validated_data.pop('password2')  # Remove password2 as it's not needed
        return User.objects.create_user(**validated_data)
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,max_length=255)
    password = serializers.CharField(write_only=True,max_length=128)
    full_name = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'full_name',
            'access_token',
            'refresh_token',
        ]

        read_only_fields = ["id"]

    def validate(self, attrs: dict) -> dict:
        email = attrs.get('email')
        password =  attrs.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed(_("Invalid email or password. Please try again."))
        
        if not user.is_active:
            raise AuthenticationFailed(_("This account is inactive. Please contact support."))
        
        tokens = user.tokens()

        return {
            'email': user.email,
            'full_name': user.full_name,
            'access_token': str(tokens.get("access")),
            'refresh_token': str(tokens.get("refresh")),
        }


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    
    def validate(self, attrs):
        """
        Validate that the refresh token is provided.
        """
        refresh_token = attrs.get("refresh_token")
        if not refresh_token:
            raise ValidationError("Refresh token is required.")
        return attrs 
    
    def save(self, **kwargs):
        """
        Blacklist the provided refresh token to log out the user.
        """
        refresh_token = self.validated_data["refresh_token"]
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            raise ValidationError("Invalid or expired refresh token.") from e
        

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    class Meta:
        model = User
        fields = [
                'email',
                ]

class SetNewPasswordSerializer(serializers.Serializer):
    """
    Serializer to handle new password submission.
    """
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs
