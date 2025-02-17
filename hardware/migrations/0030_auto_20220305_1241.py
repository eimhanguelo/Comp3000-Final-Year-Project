# Generated by Django 3.2.7 on 2022-03-05 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0029_auto_20220305_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalphone',
            name='provided_ip',
            field=models.GenericIPAddressField(blank=True, db_index=True, null=True, verbose_name='Phone IP'),
        ),
        migrations.AddField(
            model_name='phone',
            name='provided_ip',
            field=models.GenericIPAddressField(blank=True, null=True, unique=True, verbose_name='Phone IP'),
        ),
    ]
