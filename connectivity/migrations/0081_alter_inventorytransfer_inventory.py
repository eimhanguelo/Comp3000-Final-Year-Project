# Generated by Django 3.2.7 on 2022-08-31 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0068_alter_inventory_attachment'),
        ('connectivity', '0080_alter_inventorytransfer_lantransfer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventorytransfer',
            name='inventory',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='inventory_transfer', to='hardware.inventory'),
        ),
    ]
