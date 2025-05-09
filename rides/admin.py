from django.contrib import admin
from .models import Ride, Booking, Notification, Rating, Message

# Register your models here.
admin.site.register(Ride)
admin.site.register(Booking)
admin.site.register(Notification)
admin.site.register(Rating)
admin.site.register(Message)
