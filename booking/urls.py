from django.urls import path
from .views import ClassListView, BookingCreateView, BookingListByEmail
from .views import CreateFitnessClassView
from .views import AllBookingsView
from .views import CancelBookingView, CancelClassView

urlpatterns = [
    path('classes/', ClassListView.as_view(), name='class-list'),
    path('book/', BookingCreateView.as_view(), name='booking-create'),
    path('create-class/', CreateFitnessClassView.as_view(), name='create-class'),
    path('bookings/', BookingListByEmail.as_view(), name='booking-by-email'),
    path('all-bookings/', AllBookingsView.as_view(), name='all-bookings'),
    path('cancel-booking/<int:id>/', CancelBookingView.as_view(), name='cancel-booking'),
    path('cancel-class/<int:id>/', CancelClassView.as_view(), name='cancel-class'),
]