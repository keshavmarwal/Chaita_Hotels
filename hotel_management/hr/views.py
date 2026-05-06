from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q
from .models import Employee, Shift, Attendance
from .serializers import EmployeeSerializer, ShiftSerializer, AttendanceSerializer


class EmployeeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role not in ["ADMIN", "HR"]:
            return Response({"error": "Permission denied"}, status=403)
        employees = Employee.objects.filter(is_active=True)
        return Response(EmployeeSerializer(employees, many=True).data)

    def post(self, request):
        if request.user.role not in ["ADMIN", "HR"]:
            return Response({"error": "Permission denied"}, status=403)
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Employee added", "data": serializer.data})
        return Response(serializer.errors, status=400)


class EmployeeDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        if request.user.role not in ["ADMIN", "HR"]:
            return Response({"error": "Permission denied"}, status=403)
        try:
            employee = Employee.objects.get(id=pk)
            serializer = EmployeeSerializer(employee, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"msg": "Employee updated", "data": serializer.data})
            return Response(serializer.errors, status=400)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)

    def delete(self, request, pk):
        if request.user.role not in ["ADMIN", "HR"]:
            return Response({"error": "Permission denied"}, status=403)
        try:
            employee = Employee.objects.get(id=pk)
            employee.is_active = False  # soft delete
            employee.save()
            return Response({"msg": "Employee deactivated"})
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)


class ShiftView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role not in ["ADMIN", "HR"]:
            return Response({"error": "Permission denied"}, status=403)
        shifts = Shift.objects.select_related("employee").all()
        return Response(ShiftSerializer(shifts, many=True).data)

    def post(self, request):
        if request.user.role not in ["ADMIN", "HR"]:
            return Response({"error": "Permission denied"}, status=403)
        serializer = ShiftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Shift assigned", "data": serializer.data})
        return Response(serializer.errors, status=400)


class AttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role not in ["ADMIN", "HR"]:
            return Response({"error": "Permission denied"}, status=403)
        attendance = Attendance.objects.select_related("employee").all()
        return Response(AttendanceSerializer(attendance, many=True).data)

    def post(self, request):
        if request.user.role not in ["ADMIN", "HR"]:
            return Response({"error": "Permission denied"}, status=403)
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Attendance marked", "data": serializer.data})
        return Response(serializer.errors, status=400)


class HRReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role not in ["ADMIN", "HR"]:
            return Response({"error": "Permission denied"}, status=403)

        total_employees = Employee.objects.filter(is_active=True).count()

        # Attendance summary
        attendance_summary = Attendance.objects.values("status").annotate(
            count=Count("id")
        )

        # Per employee attendance
        employees = Employee.objects.filter(is_active=True)
        employee_report = []
        for emp in employees:
            total = Attendance.objects.filter(employee=emp).count()
            present = Attendance.objects.filter(employee=emp, status="present").count()
            absent = Attendance.objects.filter(employee=emp, status="absent").count()
            late = Attendance.objects.filter(employee=emp, status="late").count()

            employee_report.append({
                "id": emp.id,
                "name": emp.name,
                "role": emp.role,
                "total_days": total,
                "present": present,
                "absent": absent,
                "late": late,
                "attendance_rate": round((present / total) * 100, 2) if total > 0 else 0
            })

        return Response({
            "total_employees": total_employees,
            "attendance_summary": attendance_summary,
            "employee_report": employee_report,
        })