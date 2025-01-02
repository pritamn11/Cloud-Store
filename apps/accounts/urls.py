from .views import (
    RegisterUserAPIView,
    LoginUserAPIView,
    LogoutUserAPIView,
    RequestPasswordResetAPIView,
    PasswordResetVerifyAPIView,
    SetNewPasswordAPIView
                    )

from rest_framework_simplejwt.views import token_refresh

from django.urls import path 

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('login/', LoginUserAPIView.as_view(), name='login'),
    path('logout/', LogoutUserAPIView.as_view(), name='logout'),
    path('password-reset-request/', RequestPasswordResetAPIView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetVerifyAPIView.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPasswordAPIView.as_view(), name='set-new-password'),

    path('token/refresh/', token_refresh, name='token_refresh'),
]