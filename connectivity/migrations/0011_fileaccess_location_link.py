# Generated by Django 3.1.7 on 2021-06-12 21:07

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connectivity', '0010_auto_20210409_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileaccess',
            name='location_link',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None),
        ),
    ]
