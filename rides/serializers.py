from rest_framework import serializers
from .models import Ride, Booking

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'origin', 'destination', 'departure_time', 'seats_available', 'fare', 'created_at']
        read_only_fields = ['id', 'created_at']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'ride', 'seats_booked', 'booked_at']
        read_only_fields = ['id', 'booked_at']