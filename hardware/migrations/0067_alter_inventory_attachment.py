# Generated by Django 3.2.7 on 2022-08-28 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0066_auto_20220825_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='chalan copy', verbose_name='Chalan Hard Copy'),
        ),
    ]
