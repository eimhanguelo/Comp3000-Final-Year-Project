# Generated by Django 3.2.7 on 2022-08-24 12:30

from django.db import migrations, models
import hardware.models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0057_auto_20220824_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='chalan_copy',
            field=models.FileField(blank=True, max_length=254, null=True, upload_to=hardware.models.user_directory_path, verbose_name='Chalan Hard Copy'),
        ),
    ]
