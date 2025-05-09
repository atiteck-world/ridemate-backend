from django.core.management.base import BaseCommand
from users.models import User, DriverProfile, PassengerProfile
from rides.models import Ride, Booking
from django.utils import timezone
from datetime import timedelta
import random
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Seed the database with sample users, profiles, rides, and bookings'

    def handle(self, *args, **kwargs):
        # Optional: Clear old test data
        print("🧹 Clearing old data...")
        Booking.objects.all().delete()
        Ride.objects.all().delete()
        DriverProfile.objects.all().delete()
        PassengerProfile.objects.all().delete()
        User.objects.all().delete()

        print("🚗 Creating drivers...")
        for i in range(3):
            user, created = User.objects.get_or_create(
                username=f'driver{i}',
                defaults={
                    'email': f'driver{i}@mail.com',
                    'is_driver': True,
                    'phone_number': f'05500000{i}',
                }
            )
            user.set_password('password')
            user.save()

            DriverProfile.objects.get_or_create(
                user=user,
                defaults={
                    'license_number': f'DRV-LIC-{i+1}',
                    'vehicle_model': 'Toyota Corolla',
                    'vehicle_color': random.choice(['Red', 'Black', 'Blue']),
                    'vehicle_number': f'GR-12{i+1}-25',
                    'bio': 'Experienced driver with clean record.'
                }
            )
            Token.objects.get_or_create(user=user)

        print("🧍 Creating passengers...")
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'passenger{i}',
                defaults={
                    'email': f'passenger{i}@mail.com',
                    'is_driver': False,
                    'phone_number': f'02400000{i}',
                }
            )
            user.set_password('password')
            user.save()

            PassengerProfile.objects.get_or_create(
                user=user,
                defaults={
                    'bio': 'Frequent rider and app user.'
                }
            )
            Token.objects.get_or_create(user=user)

        print("📅 Creating rides...")
        drivers = User.objects.filter(is_driver=True)
        for i in range(10):
            Ride.objects.create(
                driver=random.choice(drivers),
                origin=random.choice(['Accra', 'Kumasi', 'Tamale']),
                destination=random.choice(['Cape Coast', 'Sunyani', 'Ho']),
                departure_time=timezone.now() + timedelta(days=random.randint(1, 10)),
                seats_available=random.randint(2, 5),
                fare=random.randint(30, 100)
            )

        print("🎟️ Creating bookings...")
        passengers = User.objects.filter(is_driver=False)
        rides = Ride.objects.all()
        for i in range(8):
            ride = random.choice(rides)
            if ride.seats_available > 0:
                seats = random.randint(1, min(ride.seats_available, 2))
                Booking.objects.create(
                    ride=ride,
                    passenger=random.choice(passengers),
                    seats_booked=seats
                )
                ride.seats_available -= seats
                ride.save()

        self.stdout.write(self.style.SUCCESS('✅ Seeded users, profiles, rides, and bookings successfully.'))
