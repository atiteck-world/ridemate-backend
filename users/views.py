
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from users.models import DriverProfile, PassengerProfile
from .serializers import DriverProfileSerializer, PassengerProfileSerializer, UserRegistrationSerializer, UserProfileSerializer, PublicDriverProfileSerializer
from .models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "User registered successfully.",
                "token": token.key
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            })
        return Response({"Error": "invalid username or passsword"}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({'message': 'User delete successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class DriverProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_driver:
            return Response({"error": "Only drivers have a driver profile."}, status=403)

        profile, created = DriverProfile.objects.get_or_create(user=request.user)
        serializer = DriverProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        if not request.user.is_driver:
            return Response({"error": "Only drivers can update this profile."}, status=403)

        profile, created = DriverProfile.objects.get_or_create(user=request.user)

        serializer = DriverProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Driver profile updated.", "data": serializer.data})
        return Response(serializer.errors, status=400)
    
class PassengerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_driver:
            return Response({"error": "Only passengers have a passenger profile."}, status=403)

        profile, _ = PassengerProfile.objects.get_or_create(user=request.user)
        serializer = PassengerProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        if request.user.is_driver:
            return Response({"error": "Only passengers can update this profile."}, status=403)

        profile, _ = PassengerProfile.objects.get_or_create(user=request.user)
        serializer = PassengerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Passenger profile updated.", "data": serializer.data})
        return Response(serializer.errors, status=400)
    
class PublicDriverProfileView(RetrieveAPIView):
    queryset = DriverProfile.objects.select_related('user')
    serializer_class = PublicDriverProfileSerializer
    permission_classes = [AllowAny]
    lookup_field = 'user_id'

class DriverListView(ListAPIView):
    queryset = DriverProfile.objects.select_related('user').order_by('user__username')
    serializer_class = PublicDriverProfileSerializer
    permission_classes = [AllowAny]
