# Generated by Django 3.2.7 on 2024-09-01 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0097_product_transfer_list_item'),
        ('connectivity', '0087_auto_20240827_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lantransfer',
            name='transfer_list',
            field=models.ManyToManyField(blank=True, to='hardware.Product'),
        ),
    ]
