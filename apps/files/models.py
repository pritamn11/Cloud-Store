from django.db import models
from apps.accounts.models import User
from django.utils.translation import gettext_lazy as _
from apps.folders.models import Folder

# Create your models here.
class File(models.Model):
    user = models.ForeignKey(User, related_name='files', on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, related_name='files', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='user_files/')
    size = models.PositiveIntegerField()  # Size in bytes
    file_type = models.CharField(max_length=50,default='Unknown Type')
    location = models.CharField(max_length=1024, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Compute the location based on the folder's location
        if self.folder:
            self.location = f"{self.folder.location}/{self.name}"
        else:
            self.location = "CloudStore"  # Default location for files not in a folder
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')