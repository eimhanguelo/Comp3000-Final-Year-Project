# Generated by Django 3.2.7 on 2024-06-19 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0090_delete_requisitionasset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisitionacc',
            name='requisition',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='requisition_accountant', to='hardware.requisition'),
        ),
    ]
