from rest_framework import viewsets
from .models import Leave
from leave_management.serializers import LeaveSerializer
from rest_framework.permissions import IsAuthenticated

class LeaveViewSet(viewsets.ModelViewSet):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        employee_id = self.request.query_params.get('employee_id', None)
        year = self.request.query_params.get('year', None)
        
        queryset = super().get_queryset()
        
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)
        if year:
            queryset = queryset.filter(year=year)
        
        return queryset.order_by('month')