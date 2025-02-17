# Generated by Django 3.2.7 on 2024-12-10 11:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20241130_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalprofile',
            name='emp_join_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='historicalprofile',
            name='is_accountant',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='historicalprofile',
            name='is_hod_it',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='historicalprofile',
            name='is_hr',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='historicalprofile',
            name='is_productivity_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='historicalprofile',
            name='is_verifier_it',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='emp_join_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_accountant',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_hod_it',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_hr',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_productivity_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_verifier_it',
            field=models.BooleanField(default=False),
        ),
    ]
