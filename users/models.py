from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    is_driver = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, unique=True)
    car_model = models.CharField(max_length=50, blank=True, null=True)


def __str__(self):
    return self.username
