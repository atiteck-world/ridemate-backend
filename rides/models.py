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
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]

    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='bookings')
    passenger = models.ForeignKey('users.User', on_delete=models.CASCADE)
    seats_booked = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['ride', 'passenger']

    def __str__(self):
        return f"{self.passenger.username} booked {self.seats_booked} seat(s) on Ride {self.ride.id}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To {self.user.username} - {self.message[:30]}..."
    
class Rating(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='ratings')
    passenger = models.ForeignKey('users.User', on_delete=models.CASCADE)
    driver = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='received_ratings')
    score = models.PositiveSmallIntegerField()
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ride', 'passenger')


    def __str__(self):
        return f"{self.passenger.username} rated {self.driver.username} - {self.score}"
    
class Message(models.Model):
    sender = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}: {self.content[:30]}"


