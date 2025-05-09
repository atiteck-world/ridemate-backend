
from rest_framework import serializers
from .models import Ride, Booking, User, Notification, Rating, Message

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

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'ride', 'passenger', 'driver', 'score', 'review', 'created_at']
        read_only_fields = ['id', 'passenger', 'driver', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'is_read', 'timestamp']
        read_only_fields = ['id', 'sender', 'is_read', 'timestamp']