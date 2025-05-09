import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class User(AbstractUser):
    is_driver = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, unique=True)
    car_model = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username

class DriverProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=30, unique=True)
    vehicle_model = models.CharField(max_length=50)
    vehicle_color = models.CharField(max_length=30)
    vehicle_number = models.CharField(max_length=20, unique=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to='driver_profiles/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s driver profile"
    
class PassengerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='passenger_profile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to='passenger_profiles/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s passenger profile"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    # Skip during management commands like seed_data
    if os.environ.get('RUN_MAIN') != 'true':
        return

    if created:
        if instance.is_driver and not hasattr(instance, 'driver_profile'):
            DriverProfile.objects.create(user=instance)
        elif not instance.is_driver and not hasattr(instance, 'passenger_profile'):
            PassengerProfile.objects.create(user=instance)
