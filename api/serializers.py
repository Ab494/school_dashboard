# API serializers for the School Dashboard application
# This file contains serializers for the Student model, which is used to convert complex data types,
# such as querysets and model instances, into native Python data types that can then be easily
from rest_framework import serializers
from core.models import Student
#Serializer for the Student model
#This serializer will handle the conversion of Student model instances to JSON format and vice versa.

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'