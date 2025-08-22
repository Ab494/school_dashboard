from doctest import Example
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone

class Student(models.Model):
    name = models.CharField(max_length=100)
    class_level = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    admission_number = models.CharField(max_length=20, unique=True)
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)
    def __str__(self):
        return self.name

class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    def __str__(self):
        return f"{self.full_name()} - {self.subject}"
    
STATUS_CHOICES = [
    ('Present', 'Present'),
    ('Absent', 'Absent'),

]
class Attendance(models.Model):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"
    
    
class Unit(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.code} - {self.name}"

    
    

    
    
