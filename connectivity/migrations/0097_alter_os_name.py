# Generated by Django 3.2.7 on 2024-12-14 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connectivity', '0096_auto_20240915_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='os',
            name='name',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
