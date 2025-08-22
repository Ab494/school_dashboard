# This file is part of the School Dashboard project.
from django import template 
register = template.Library() 

# This template tag is used to render a form field with a specific class. 
@register.filter(name= 'add_class') 
def add_class(value, arg):
    return value.as_widget(attrs={'class': arg})
