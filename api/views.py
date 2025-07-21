# API views for the school_dashboard project.
# This file will contain view classes or functions for handling API requests,
# such as listing, creating, updating, or deleting resources via the REST API.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import StudentSerializer
from core.models import Student

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    
