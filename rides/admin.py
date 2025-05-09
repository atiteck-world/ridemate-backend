from django.contrib import admin
from .models import Ride, Booking, Notification

# Register your models here.
admin.site.register(Ride)
admin.site.register(Booking)
admin.site.register(Notification)
