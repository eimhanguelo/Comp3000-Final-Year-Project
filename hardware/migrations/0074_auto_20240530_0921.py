# Generated by Django 3.2.7 on 2024-05-30 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0073_auto_20240530_0841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalinventory',
            name='model',
        ),
        migrations.RemoveField(
            model_name='historicalinventory',
            name='unit_type',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='model',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='unit_type',
        ),
    ]
