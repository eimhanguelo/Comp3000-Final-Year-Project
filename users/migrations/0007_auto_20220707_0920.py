# Generated by Django 3.2.7 on 2022-07-07 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20220707_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalprofile',
            name='is_hr',
            field=models.BooleanField(null=True, verbose_name='HR Status'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='is_hr',
            field=models.BooleanField(null=True, verbose_name='HR Status'),
        ),
    ]
