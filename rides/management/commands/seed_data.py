from django.core.management.base import BaseCommand
from users.models import User
from rides.models import Ride, Booking
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Seed the database with sample users, rides, and bookings'

    def handle(self, *args, **kwargs):
        # Create drivers
        for i in range(3):
            user, _ = User.objects.get_or_create(
                username=f'driver{i}',
                defaults={
                    'email': f'driver{i}@mail.com',
                    'is_driver': True,
                    'phone_number': f'05500000{i}',
                    'car_model': 'Toyota Corolla',
                    'password': 'password'
                }
            )
            user.set_password('password')
            user.save()

        # Create passengers
        for i in range(5):
            user, _ = User.objects.get_or_create(
                username=f'passenger{i}',
                defaults={
                    'email': f'passenger{i}@mail.com',
                    'is_driver': False,
                    'phone_number': f'02400000{i}',
                    'password': 'password'
                }
            )
            user.set_password('password')
            user.save()

        # Create rides
        drivers = User.objects.filter(is_driver=True)
        for i in range(10):
            Ride.objects.create(
                driver=random.choice(drivers),
                origin=random.choice(['Accra', 'Kumasi', 'Takoradi']),
                destination=random.choice(['Cape Coast', 'Tamale', 'Koforidua']),
                departure_time=timezone.now() + timedelta(days=random.randint(1, 10)),
                seats_available=random.randint(2, 5),
                fare=random.randint(30, 100)
            )

        # Create bookings
        passengers = User.objects.filter(is_driver=False)
        rides = Ride.objects.all()
        for i in range(10):
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

        self.stdout.write(self.style.SUCCESS('Seeded users, rides, and bookings.'))
