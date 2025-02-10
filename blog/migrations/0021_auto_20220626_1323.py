# Generated by Django 3.2.7 on 2022-06-26 13:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_alter_resignationsign_signing_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='historicalaccount',
            name='date_updated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False),
            preserve_default=False,
        ),
    ]
