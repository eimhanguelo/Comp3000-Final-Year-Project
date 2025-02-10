# Generated by Django 3.2.7 on 2022-08-17 16:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hardware', '0045_alter_inventory_product_condition'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='chalan_copy',
            field=models.FileField(blank=True, null=True, upload_to='Chalan', verbose_name='Chalan Hard Copy'),
        ),
        migrations.AddField(
            model_name='inventory',
            name='used_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inventory_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
