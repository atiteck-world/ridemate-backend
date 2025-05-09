from rest_framework import serializers
from .models import DriverProfile, PassengerProfile, User
from django.contrib.auth.password_validation import validate_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'is_driver', 'car_model', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'is_driver', 'car_model']

class DriverProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverProfile
        fields = [
            'license_number',
            'vehicle_model',
            'vehicle_color',
            'vehicle_number',
            'bio',
            'profile_picture',
            'created_at'
        ]
        read_only_fields = ['created_at']

class PassengerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerProfile
        fields = ['bio', 'profile_picture', 'created_at']
        read_only_fields = ['created_at']

class PublicDriverProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    
    class Meta:
        model = DriverProfile
        fields = ['id', 'username', 'phone_number', 'profile_picture', 'bio', 'vehicle_model', 'vehicle_number', 'vehicle_color']