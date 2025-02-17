# Generated by Django 3.2.7 on 2022-08-28 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connectivity', '0076_auto_20220824_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicallan',
            name='instrument_id',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Instrument ID'),
        ),
        migrations.AddField(
            model_name='historicallan',
            name='instrument_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Instrument Name'),
        ),
        migrations.AddField(
            model_name='lan',
            name='instrument_id',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Instrument ID'),
        ),
        migrations.AddField(
            model_name='lan',
            name='instrument_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Instrument Name'),
        ),
    ]
