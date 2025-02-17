# Generated by Django 3.2.7 on 2024-02-28 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0070_auto_20220906_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalinventory',
            name='attachment',
            field=models.TextField(max_length=100, verbose_name='Chalan Hard Copy'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='attachment',
            field=models.FileField(upload_to='inventory', verbose_name='Chalan Hard Copy'),
        ),
    ]
