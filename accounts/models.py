from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = None
    
    def get_email_field_name(self):
        return None
    
class ManagerUser(CustomUser):
    class Meta:
        proxy = True

    def has_manager_permissions(self):
        """Check if user has manager-specific permissions"""
        return self.is_staff or self.is_superuser
