from django.contrib import admin
from .models import Unit
# Register your models here.

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'teacher', 'teacher_group']

    def teacher_group(self, obj):
        if obj.teacher:
            return ", ".join([group.name for group in obj.teacher.groups.all()])
        return "_"
    teacher_group.short_description = "Teacher Group"
