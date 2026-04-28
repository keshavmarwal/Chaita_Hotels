from django.urls import path
from .views import BookingCreateView , CheckInView, CheckOutView, BookingListView

urlpatterns = [
    path('create/', BookingCreateView.as_view()),
    path('checkin/<int:pk>/', CheckInView.as_view()),
    path('checkout/<int:pk>/', CheckOutView.as_view()),
    path('list/', BookingListView.as_view()),
]