from django.contrib import admin
from .models import Department, Designation, Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'department', 'designation')
    search_fields = ['name']
    list_filter = ('department',)

admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Employee, EmployeeAdmin)