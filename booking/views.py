from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
import pytz

# ✅ View all bookings (optional filter by status)
class AllBookingsView(generics.ListAPIView):
    serializer_class = BookingSerializer

    def get_queryset(self):
        status_param = self.request.query_params.get('status')
        if status_param in ['active', 'cancelled']:
            return Booking.objects.filter(status=status_param)
        return Booking.objects.all()

# ✅ Create a new fitness class (for testing/demo via Postman)
class CreateFitnessClassView(generics.CreateAPIView):
    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer

# ✅ GET /classes/?status=cancelled&tz=Asia/Kolkata
class ClassListView(generics.ListAPIView):
    serializer_class = FitnessClassSerializer

    def get_queryset(self):
        queryset = FitnessClass.objects.all()

        # Optional status filter
        status_param = self.request.query_params.get('status')
        if status_param:
            status_param = status_param.lower().strip()
            queryset = queryset.filter(status__iexact=status_param)

        # Optional timezone
        tz = self.request.query_params.get('tz')
        try:
            timezone = pytz.timezone(tz) if tz else pytz.UTC
        except pytz.UnknownTimeZoneError:
            timezone = pytz.UTC

        for obj in queryset:
            obj.client_timezone = timezone

        return queryset

# ✅ POST /book/ - Book a fitness class
class BookingCreateView(generics.CreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# ✅ GET /bookings/?email=asif@gmail.com
class BookingListByEmail(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({"error": "Email query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        bookings = Booking.objects.filter(client_email=email)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ✅ POST /cancel-booking/<id>/ - Client cancels a booking
class CancelBookingView(APIView):
    def post(self, request, id):
        try:
            booking = Booking.objects.get(id=id)
            if booking.status == 'cancelled':
                return Response({"message": "Booking is already cancelled."}, status=400)

            booking.status = 'cancelled'
            booking.save()

            # restore slot
            booking.fitness_class.available_slots += 1
            booking.fitness_class.save()

            return Response({"message": "Booking cancelled successfully."}, status=200)

        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=404)

# ✅ POST /cancel-class/<id>/ - Instructor cancels class
class CancelClassView(APIView):
    def post(self, request, id):
        try:
            fitness_class = FitnessClass.objects.get(id=id)
            if fitness_class.status == 'cancelled':
                return Response({"message": "Class is already cancelled."}, status=400)

            # Cancel the class
            fitness_class.status = 'cancelled'
            fitness_class.save()

            # Cancel related bookings
            affected_bookings = Booking.objects.filter(fitness_class=fitness_class, status='active')
            for booking in affected_bookings:
                booking.status = 'cancelled'
                booking.save()

            return Response({
                "message": f"Class '{fitness_class.name}' cancelled. {affected_bookings.count()} bookings updated."
            })

        except FitnessClass.DoesNotExist:
            return Response({"error": "Class not found."}, status=404)