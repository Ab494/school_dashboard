# Generated by Django 4.2.21 on 2025-06-09 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_teacher_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
