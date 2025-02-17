# Generated by Django 3.2.7 on 2024-11-30 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_hodaccess'),
    ]

    operations = [
        migrations.AddField(
            model_name='hodaccess',
            name='departments',
            field=models.ManyToManyField(related_name='hod_departments', to='users.Department'),
        ),
        migrations.AddField(
            model_name='hodaccess',
            name='locations',
            field=models.ManyToManyField(related_name='hod_locations', to='users.Location'),
        ),
        migrations.AlterUniqueTogether(
            name='hodaccess',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='hodaccess',
            name='department',
        ),
        migrations.RemoveField(
            model_name='hodaccess',
            name='location',
        ),
    ]
