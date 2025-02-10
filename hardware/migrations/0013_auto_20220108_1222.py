# Generated by Django 3.2.7 on 2022-01-08 12:22

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hardware', '0012_requisitionproducts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(1)])),
                ('details', models.CharField(blank=True, max_length=254, null=True, verbose_name='Product Details')),
                ('remarks', models.CharField(blank=True, max_length=254, null=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('requisition_condition', models.CharField(choices=[('Sent To IT', 'Sent To IT'), ('Sent To CHQ', 'Sent To CHQ'), ('Added to Inventory', 'Added to Inventory'), ('Delivery', 'Delivery')], default='Sent To IT', max_length=50, verbose_name='Requisition Condition')),
                ('rqn_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='RQN No')),
                ('chalan_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='Chalan No')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('model', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hardware.productmodel')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hardware.product')),
                ('requisition', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requisition_inventory', to='hardware.requisition')),
                ('unit_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hardware.quantityunit', verbose_name='Unit Type')),
            ],
        ),
        migrations.DeleteModel(
            name='RequisitionProducts',
        ),
    ]
