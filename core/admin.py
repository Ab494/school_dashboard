from django.contrib import admin
from .models import Unit, Teacher
# Register your models here.

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):

    list_display = ['name', 'code', 'teacher_name']
    search_fields = ['name', 'code', 'teacher__first_name', 'teacher__last_name']
    autocomplete_fields = ['teacher',]

    def teacher_name(self, obj):
        return obj.teacher.full_name if obj.teacher else '_'
    teacher_name.short_description = "Teacher"

# Teacher Admin
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ["full_name", "subject", "email"]
    search_fields = ("first_name", "last_name", "subject", "email")

    # Tell Django how to sort the synthetic "full_name" column
    def full_name(self, obj):
        return obj.full_name()
    full_name.admin_order_field = "first_name" # sort by first_name
    full_name.short_description = 'Name'
