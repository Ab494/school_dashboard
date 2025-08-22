from django import forms
from .models import Unit, Student, Teacher, Attendance
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['code', 'name', 'semester', 'teacher']

        widgets = {
            "code": forms.TextInput(attrs={"placeholder": "e.g. DRF201"}),
            "name": forms.TextInput(attrs={"placeholder": "e.g. Install Computer Software"}),
            "semester": forms.TextInput(attrs={"placeholder": "e.g. 1st Semester"}),
            "teacher": forms.Select()
            
        }

        def clean_code(self):
            code = self.clean_data["code"].strip().upper()
            if Unit.objects.filter(code=code).exists():
                raise forms.ValidationError("A unit with this code alreaddy exists. ")
            return code
                
            

# Update StudentForm to check for duplicates
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["name", "class_level", "admission_number", "email", "date_added", "photo" ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter student name'}),
            'class_level': forms.TextInput(attrs={'placeholder': 'Enter classs level'}),
            'admission_number': forms.TextInput(attrs={'placeholder': 'Enter admission number'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
            'date_added': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_admission_number(self):
        admission_number = self.cleaned_data["admission_number"]
        if Student.objects.filter(admission_number__iexact=admission_number).exists():
            raise ValidationError("A student with this amission number already exists")
        return admission_number


# TeacherForm 
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'email', 'subject']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs= {'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Enter subject'}),
        }

# AttendanceForm
class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = ['student', 'status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'student': forms.Select(attrs={'class': 'form-select'}),
        }
