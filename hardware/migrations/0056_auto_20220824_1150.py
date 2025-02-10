# Generated by Django 3.2.7 on 2022-08-24 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0055_alter_inventory_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalinventory',
            name='product_condition',
            field=models.CharField(choices=[('Requisition Raised', 'Requisition Raised'), ('Sent to CHQ', 'Sent to CHQ'), ('In Stock', 'In Stock'), ('Delivered', 'Delivered'), ('Stock OUT', 'Stock OUT')], default='Requisition Raised', max_length=50, verbose_name='Product Condition'),
        ),
        migrations.AlterField(
            model_name='inventory',
            name='product_condition',
            field=models.CharField(choices=[('Requisition Raised', 'Requisition Raised'), ('Sent to CHQ', 'Sent to CHQ'), ('In Stock', 'In Stock'), ('Delivered', 'Delivered'), ('Stock OUT', 'Stock OUT')], default='Requisition Raised', max_length=50, verbose_name='Product Condition'),
        ),
    ]
