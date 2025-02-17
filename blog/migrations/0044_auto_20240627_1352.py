# Generated by Django 3.2.7 on 2024-06-27 13:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0043_alter_employee_approved_hr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='approved_hr',
        ),
        migrations.AddField(
            model_name='employee',
            name='approved_hr',
            field=models.ManyToManyField(blank=True, related_name='approved_hr_emp', to=settings.AUTH_USER_MODEL, verbose_name='Approved HR'),
        ),
    ]
