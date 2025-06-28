from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Designation(models.Model):
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(
        Department, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    designation = models.ForeignKey(
        Designation, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    join_date = models.DateField()
    
    def __str__(self):
        return self.name