from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = None
    branch = models.CharField(max_length=255)
    
    def get_email_field_name(self):
        return None
    
class ManagerUser(CustomUser):
    class Meta:
        proxy = True

    def has_manager_permissions(self):
        """Check if user has manager-specific permissions"""
        return self.is_staff or self.is_superuser
