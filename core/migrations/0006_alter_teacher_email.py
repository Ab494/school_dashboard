# Generated by Django 4.2.21 on 2025-06-08 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_teacher_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.EmailField(default='example@example.com', max_length=254),
        ),
    ]
