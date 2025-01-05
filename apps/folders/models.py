from django.db import models
from apps.accounts.models import User
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Folder(models.Model):
    user = models.ForeignKey(User, related_name='folders', on_delete=models.CASCADE)
    parent_folder = models.ForeignKey('self', related_name='subfolders', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, default='Folder')
    location = models.CharField(max_length=1024, blank=True) 
    size = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Compute the location dynamically based on the parent folder
        if self.parent_folder:
            self.location = f"{self.parent_folder.location}/{self.name}"
        else:
            self.location = "CloudStore"  # Root location for top-level folders
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Folder')
        verbose_name_plural = _('Folders')