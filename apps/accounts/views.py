from django.shortcuts import render
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.response import Response
from rest_framework import status
from .models import User

from .serializers import (UserSerializer,
                          RegisterSerializer,
                          LoginSerializer,
                          LogoutSerializer)

# Create your views here.

class RegisterUserAPIView(APIView):
    """
    API view to handle user registration.
    """
    serializer_class = RegisterSerializer

    @extend_schema(
            summary = "Register User",
            description="""
             This endpoint creates a new user
            """,
            tags=["User Management"],
            request=RegisterSerializer,
            responses={"201": RegisterSerializer},
    )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)  
        user = serializer.save()
        
        return Response({
            "message": f"Hi {user.first_name}, thank you for signing up! Please check your email for an OTP.",
            "data": serializer.data,},
            status=status.HTTP_201_CREATED)

class LoginUserAPIView(APIView):
    """
    API view to handle user login.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to authenticate a user.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            "message":"Login successful",
            "data":serializer.data,},
            status=status.HTTP_201_CREATED
        )


class LogoutUserAPIView(APIView):
    """
    API View to handle user logout.
    """
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handle logout by blacklisting the refresh token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Logout successful."},
            status=status.HTTP_200_OK
        )