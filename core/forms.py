from django import forms
from .models import Unit, Student
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['code', 'name', 'semester', 'teacher']

# Update StudentForm to check for duplicates
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "class_level", "admission_number", "email", "date_added", "photo_url" ]

    def clean_admission_number(self):
        admission_number = self.cleaned_data["admission_number"]
        if Student.objects.filter(admission_number__iexact=admission_number).exists():
            raise ValidationError("A student with this amission number already exists")
        return admission_number




    
