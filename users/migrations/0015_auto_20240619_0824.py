# Generated by Django 3.2.7 on 2024-06-19 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20240603_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalprofile',
            name='is_accountant',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalprofile',
            name='is_verifier_it',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_accountant',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_verifier_it',
            field=models.BooleanField(default=False),
        ),
    ]
