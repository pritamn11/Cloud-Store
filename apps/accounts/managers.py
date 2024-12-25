from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.validators import validate_email 
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def email_validator(self, email: str) -> None:
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Please provide a valid email address."))
    
    def create_user(self, first_name: str, last_name: str, email: str, password: str, **extra_fields):
        if email is None:
            raise ValueError(_("An email address is required."))
        
        email = self.normalize_email(email)
        self.email_validator(email)

        if not first_name or not last_name:
            raise ValueError(_("First name and last name are required."))
        
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    def create_superuser(self, first_name: str, last_name: str, email: str, password: str, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValidationError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        
        return self.create_user(first_name, last_name, email, password, **extra_fields)