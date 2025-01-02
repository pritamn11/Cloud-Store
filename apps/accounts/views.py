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
from rest_framework.exceptions import ValidationError
import threading
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse

from .serializers import (UserSerializer,
                          RegisterSerializer,
                          LoginSerializer,
                          LogoutSerializer,
                          PasswordResetRequestSerializer,
                          SetNewPasswordSerializer)

# Create your views here.

class RegisterUserAPIView(APIView):
    """
    API view to handle user registration.
    """
    serializer_class = RegisterSerializer

    @extend_schema(
            summary = "Register new User",
            description="""
             This endpoint creates a new user
            """,
            tags=["Register User"],
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


class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()

class RequestPasswordResetAPIView(APIView):
    """
    API View to handle user reset password request.
    """
    serializer_class = PasswordResetRequestSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("User with the provided email does not exist.")

        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        site_domain =  request.get_host()

        #Url that calls our reset password view
        relative_url = reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token})

        #url that will be displayed in the email message
        reset_link = f"http://{site_domain}{relative_url}"

        subject = "Password Reset Request"

        message_body = (
            f"Hi {user.full_name},\n\n"
            f"Reset your password using the link below:\n\n"
            f"{reset_link}\n\n"
            f"If this wasn't you, ignore this email.\n\n"
            f"Thanks!"
        )

        email_message = EmailMessage(
            subject, 
            message_body,
            settings.EMAIL_HOST_USER, 
            [email])
        email_message.send(fail_silently=False)

        # Send email in a separate thread
        EmailThread(email_message).start()

        return Response(
            { "message": "Password reset email sent successfully."},
            status=status.HTTP_200_OK
        )

    
#     def post(self, request):
#         email = request.data['to']
#         emailw = EmailMessage(
#             'Test email from cloudstore',
#             'Test email body...',
#             settings.EMAIL_HOST_USER,
#             [email]
#         )
#         emailw.send(fail_silently=False)
#         return Response({"message": "Password reset email sent successfully."},status=status.HTTP_200_OK)




class PasswordResetVerifyAPIView(APIView):
    """
    API View to verify the reset password token and user ID.
    """
    def get(self,request, uidb64, token):
        user_id = smart_str(urlsafe_base64_decode(uidb64))
        try:
            # Decode the UID
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            # Validate the token
            if PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    "message": "Credentials validated successfully",
                    "data": {
                        "token": token,
                        "uidb64": uidb64
                    }
                }, status=status.HTTP_200_OK)
            
            return Response({"message": "Token is invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)

        except (DjangoUnicodeDecodeError, User.DoesNotExist):
            return Response({"message": "Invalid user or token"}, status=status.HTTP_404_NOT_FOUND)
        

class SetNewPasswordAPIView(APIView):
    """
    API View to set the new password using a valid token and user ID.
    """
    serializer_class = SetNewPasswordSerializer

    def post(self, request, uidb64, token):
        try:
            # Decode the UID
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            # Validate the token
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"message": "Token is invalid or expired"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate new password data
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Set the new password
            user.set_password(serializer.validated_data['password'])
            user.save()

            return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)

        except (DjangoUnicodeDecodeError, User.DoesNotExist, ValidationError):
            return Response({"message": "Invalid user or token"}, status=status.HTTP_404_NOT_FOUND)