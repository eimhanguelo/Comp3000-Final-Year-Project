# Generated by Django 3.2.7 on 2022-01-05 15:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hardware', '0004_requisition'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisition',
            name='asset_no',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Asset No'),
        ),
        migrations.AddField(
            model_name='requisition',
            name='asset_provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='asset_provider', to=settings.AUTH_USER_MODEL, verbose_name='Asset No Provider'),
        ),
    ]
