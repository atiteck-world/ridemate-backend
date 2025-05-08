
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import RideSerializer
from .models import Ride

# Create your views here.

class RideCreateView(APIView):
    permission_classes = [IsAuthenticated]

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