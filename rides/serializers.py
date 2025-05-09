from rest_framework import serializers
from .models import Ride, Booking, User, Notification

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'origin', 'destination', 'departure_time', 'seats_available', 'fare', 'created_at']
        read_only_fields = ['id', 'created_at']

class RideSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'origin', 'destination', 'departure_time', 'fare']

class PassengerSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number']

class BookingSerializer(serializers.ModelSerializer):
    ride = RideSummarySerializer(read_only=True)
    passenger = PassengerSummarySerializer(read_only=True)
    class Meta:
        model = Booking
        fields = ['id', 'ride', 'passenger', 'seats_booked', 'booked_at']
        #read_only_fields = ['id', 'booked_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'message', 'is_read', 'created_at']
