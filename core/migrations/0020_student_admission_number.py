# Generated by Django 4.2.21 on 2025-06-16 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_student_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='admission_number',
            field=models.CharField(default='TEMP', max_length=20),
        ),
    ]
