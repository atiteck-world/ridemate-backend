
from django.forms import ValidationError
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, serializers
from .serializers import MessageSerializer, RatingSerializer, RideSerializer, BookingSerializer, NotificationSerializer
from .models import Rating, Ride, Booking, Notification, Message
from .permissions import IsDriver, IsPassenger
from django.db.models import Q
from django.db.models import Max
from django.utils import timezone


# Create your views here.

class RideCreateView(APIView):
    permission_classes = [IsAuthenticated, IsDriver]

    def post(self, request):
        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(driver=request.user)
                return Response({
                    "message": "Ride posted Successflly",
                    "ride": serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                print("ride creation error:", e)
                return Response({"error": str( e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
class RideListView(ListAPIView):
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        queryset = Ride.objects.all().order_by('-created_at')

        origin = self.request.query_params.get('origin')
        destination = self.request.query_params.get('destination')
        date = self.request.query_params.get('date')

        if origin:
            queryset = queryset.filter(origin__icontains=origin)

        if destination:
            queryset = queryset.filter(destination__icontains=destination)

        if date:
            queryset = queryset.filter(date__icontains=date)

        return queryset
    
class RideDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(driver=self.request.user)
    
class BookRideView(APIView):
    permission_classes = [IsAuthenticated, IsPassenger]

    def post(self, request, ride_id):
        try:
            ride = Ride.objects.get(pk=ride_id)
        except Ride.DoesNotExist:
            return Response({"error": "Ride not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            seats_requested = int(request.data.get('seats_booked', 1))
            if seats_requested < 1:
                raise ValueError("Seats requested must be at least 1.")
        except (ValueError, TypeError):
            return Response({"error": "Invalid number of seats requested."}, status=status.HTTP_400_BAD_REQUEST)

        if ride.seats_available < seats_requested:
            return Response({"error": "Not enough seats available."}, status=status.HTTP_400_BAD_REQUEST)
        
        # create booking
        booking = Booking.objects.create(
            ride = ride,
            passenger = request.user,
            seats_booked=seats_requested
        )
        # Notify driver
        Notification.objects.create(
            user=ride.driver,
            message=f"{request.user.username} booked {seats_requested} seat(s) on your ride {ride.origin} to {ride.destination}."
        )

        #print(f"Notification: {request.user.username} booked {seats_requested} seat(s) on your ride from {ride.origin} to {ride.destination}.")

        # Notify passenger
        Notification.objects.create(
            user=request.user,
            message=f"You booked {seats_requested} seat(s) from {ride.origin} to {ride.destination}."
        )
        #print(f"You booked {seats_requested} seat(s) from {ride.origin} to {ride.destination} for GH₵{ride.fare}.")


        ride.seats_available -= seats_requested
        ride.save()

        return Response({
            "message": "Ride booked successfully.",
            "booking": BookingSerializer(booking).data
        }, status=status.HTTP_201_CREATED)
    
class MyBookingsView(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(passenger=self.request.user).order_by('-booked_at')
    
class CancelBookingView(DestroyAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(passenger=self.request.user)
    
    def perform_destroy(self, instance):
        ride = instance.ride
        ride.seats_available += instance.seats_booked
        ride.save()
        instance.delete()

        Notification.objects.create(
            user = instance.ride.driver,
            message = f"{self.request.user.username} canceled their booking on your ride from {instance.ride.origin} to {instance.ride.destination}."
        )

        Notification.objects.create(
            user = self.request.user,
            message = f"You canceled your booking from {instance.ride.origin} to {instance.ride.destination}."
        )
        #print(f"{self.request.user.username} canceled their booking for ride {instance.ride.id}.")

class DriverRideBookingView(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        #Get all rides created by the logged-in driver
        driver_rides = Ride.objects.filter(driver=self.request.user)

        #Return bookings made on those rides
        return Booking.objects.filter(ride__in=driver_rides).order_by('-booked_at')
    
class UserNotificationView(ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class SubmitRatingView(CreateAPIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        ride_id = self.request.data.get('ride')
        if not ride_id:
            raise ValidationError({"ride": "Ride ID is required."})

        try:
            ride = Ride.objects.get(id=ride_id)
        except Ride.DoesNotExist:
            raise ValidationError({"ride": "Ride not found."})

        if ride.driver == self.request.user:
            raise ValidationError("Drivers cannot rate themselves.")

        # Check if this user already rated this ride
        if Rating.objects.filter(ride=ride, passenger=self.request.user).exists():
            raise ValidationError("You have already rated this ride.")

        serializer.save(
            ride=ride,
            passenger=self.request.user,
            driver=ride.driver
        )

class DriverRatingListView(ListAPIView):
    serializer_class = RatingSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        driver_id = self.kwargs['driver_id']
        return Rating.objects.filter(driver__id=driver_id).order_by('-created_at')
    
class SendMessageView(CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        receiver_id = self.request.data.get('receiver')
        if not receiver_id:
            raise serializers.ValidationError({"receiver": "Receiver ID is required."})

        serializer.save(sender=self.request.user)

class ChatThreadView(ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        other_user_id = self.kwargs['user_id']
        user = self.request.user

        return Message.objects.filter(
            (Q(sender=user) & Q(receiver_id=other_user_id)) |
            (Q(sender_id=other_user_id) & Q(receiver=user))
        ).order_by('timestamp')
    
class InboxView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Get latest message per conversation
        latest_messages_ids = (
            Message.objects
            .filter(Q(sender=user) | Q(receiver=user))
            .values('sender', 'receiver')
            .annotate(latest_id=Max('id'))
            .values_list('latest_id', flat=True)
        )

        messages = Message.objects.filter(id__in=latest_messages_ids).order_by('-timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
class RideHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        now = timezone.now()

        if user.is_driver:
            rides = Ride.objects.filter(driver=user)
        else:
            rides = Ride.objects.filter(bookings__passenger=user).distinct()

        upcoming = rides.filter(departure_time__gt=now)
        past = rides.filter(departure_time__lt=now)

        return Response({
            "upcoming": RideSerializer(upcoming, many=True).data,
            "past": RideSerializer(past, many=True).data
        })