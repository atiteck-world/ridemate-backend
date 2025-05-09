from django.contrib import admin
from .models import User, DriverProfile, PassengerProfile

# Register your models here.
admin.site.register(User)
admin.site.register(DriverProfile)
admin.site.register(PassengerProfile)