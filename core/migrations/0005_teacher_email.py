# Generated by Django 4.2.21 on 2025-06-08 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_student_profile_picture_student_photo_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='email',
            field=models.EmailField(default='example@example.com', max_length=254, unique=True),
        ),
    ]
