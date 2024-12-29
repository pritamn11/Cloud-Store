from .views import (RegisterUserAPIView)

from rest_framework_simplejwt.views import token_refresh

from django.urls import path 

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view()),
]