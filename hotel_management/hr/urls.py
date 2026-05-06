from django.urls import path
from .views import EmployeeView, EmployeeDetailView, ShiftView, AttendanceView, HRReportView

urlpatterns = [
    path('employees/', EmployeeView.as_view()),
    path('employees/<int:pk>/', EmployeeDetailView.as_view()),
    path('shifts/', ShiftView.as_view()),
    path('attendance/', AttendanceView.as_view()),
    path('reports/', HRReportView.as_view()),
]