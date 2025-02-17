# Generated by Django 3.2.7 on 2022-08-24 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('connectivity', '0075_auto_20220822_0758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicallan',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lan',
            name='printer_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='connectivity.printermodel'),
        ),
        migrations.AlterField(
            model_name='lan',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lan',
            name='scanner_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='connectivity.scannermodel'),
        ),
    ]
