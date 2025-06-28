from django.db import models
from employees.models import Employee

class Leave(models.Model):
    LEAVE_TYPES = (
        ('SL', 'Sick Leave'),
        ('CL', 'Casual Leave'),
    )
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=2, choices=LEAVE_TYPES)
    month = models.PositiveSmallIntegerField()  # 1-12 representing months
    year = models.PositiveSmallIntegerField()
    days_taken = models.DecimalField(max_digits=3, decimal_places=1)
    applied_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('employee', 'leave_type', 'month', 'year')
    
    def __str__(self):
        return f"{self.employee.name} - {self.get_leave_type_display()}"