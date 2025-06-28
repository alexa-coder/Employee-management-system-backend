from rest_framework import viewsets, permissions
from .models import Employee, Department, Designation
from .serializers import EmployeeSerializer, DepartmentSerializer, DesignationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class DesignationViewSet(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    permission_classes = [permissions.IsAuthenticated]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().select_related('department', 'designation')
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        search_filter = self.request.query_params.get('search_filter', 'all')
        
        if search:
            if search_filter == 'all':
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(email__icontains=search) |
                    Q(department__name__icontains=search) |
                    Q(designation__title__icontains=search)
                )
            elif search_filter == 'name':
                queryset = queryset.filter(name__icontains=search)
            elif search_filter == 'email':
                queryset = queryset.filter(email__icontains=search)
            elif search_filter == 'department':
                queryset = queryset.filter(department__name__icontains=search)
            elif search_filter == 'designation':
                queryset = queryset.filter(designation__title__icontains=search)
        
        return queryset.select_related('department', 'designation')
    
    @action(detail=False, methods=['get'])
    def suggestions(self, request):
        search = request.query_params.get('search', '')
        suggestions = set()
        
        if len(search) > 2:
            # Name suggestions
            names = Employee.objects.filter(
                name__icontains=search
            ).values_list('name', flat=True).distinct()[:5]
            
            # Email suggestions
            emails = Employee.objects.filter(
                email__icontains=search
            ).values_list('email', flat=True).distinct()[:5]
            
            # Department suggestions
            departments = Department.objects.filter(
                name__icontains=search
            ).values_list('name', flat=True).distinct()[:5]
            
            # Combine all suggestions
            suggestions.update(names)
            suggestions.update(emails)
            suggestions.update(departments)
        
        return Response(list(suggestions)[:10])