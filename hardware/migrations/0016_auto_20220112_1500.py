# Generated by Django 3.2.7 on 2022-01-12 15:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hardware', '0015_auto_20220108_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='chalan',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Chalan No'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inventory_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='inventory',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inventory',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='inventory',
            name='product_condition',
            field=models.CharField(choices=[('Requisition Raised', 'Requisition Raised'), ('Sent to CHQ', 'Sent to CHQ'), ('Added to Inventory', 'Added to Inventory'), ('Delivery', 'Delivery')], default='Requisition Raised', max_length=50, verbose_name='Product Condition'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='rqn_no',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='RQN No'),
        ),
    ]
