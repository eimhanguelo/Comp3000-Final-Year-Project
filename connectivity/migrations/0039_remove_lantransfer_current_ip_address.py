# Generated by Django 3.2.7 on 2021-10-15 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connectivity', '0038_remove_lantransfer_transfer_location_old_ip'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lantransfer',
            name='current_ip_address',
        ),
    ]
