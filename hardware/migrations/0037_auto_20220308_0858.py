# Generated by Django 3.2.7 on 2022-03-08 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_historicalprofile'),
        ('hardware', '0036_auto_20220308_0853'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalphone',
            name='model',
        ),
        migrations.RemoveField(
            model_name='phone',
            name='model',
        ),
        migrations.AddField(
            model_name='historicalphone',
            name='location',
            field=models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='users.location'),
        ),
        migrations.AddField(
            model_name='phone',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.location'),
        ),
    ]
