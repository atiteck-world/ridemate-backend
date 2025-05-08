from rest_framework import serializers
from .models import Ride

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'origin', 'destination', 'departure_time', 'seats_available', 'fare', 'created_at']
        read_only_fields = ['id', 'created_at']