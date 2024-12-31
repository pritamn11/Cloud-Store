from .views import (
    RegisterUserAPIView,
    LoginUserAPIView,
    LogoutUserAPIView
                    )

from rest_framework_simplejwt.views import token_refresh

from django.urls import path 

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('login/', LoginUserAPIView.as_view(), name='login'),
    path('logout/', LogoutUserAPIView.as_view(), name='logout'),

    path('token/refresh/', token_refresh, name='token_refresh'),
]