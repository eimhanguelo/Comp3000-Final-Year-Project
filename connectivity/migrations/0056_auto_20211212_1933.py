# Generated by Django 3.2.7 on 2021-12-12 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connectivity', '0055_remove_lantransfer_transfer_location_plant'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicallan',
            name='ip_used',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lan',
            name='ip_used',
            field=models.BooleanField(default='True'),
            preserve_default=False,
        ),
    ]
