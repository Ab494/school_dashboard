from django import forms
from .models import Unit
from django.contrib.auth.models import User, Group

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['code', 'name', 'semester', 'teacher']



    
