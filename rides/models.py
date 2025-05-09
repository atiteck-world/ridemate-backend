from django.db import models
from users.models import User

# Create your models here.
class Ride(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_time = models.DateTimeField()
    seats_available = models.PositiveIntegerField()
    fare = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.origin} to {self.destination} by {self.driver.username}"
    

class Booking(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='bookings')
    passenger = models.ForeignKey('users.User', on_delete=models.CASCADE)
    seats_booked = models.PositiveIntegerField(default=1)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.passenger.username} booked {self.seats_booked} seat(s) on Ride {self.ride.id}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.user.username} - {self.message[:30]}..."

