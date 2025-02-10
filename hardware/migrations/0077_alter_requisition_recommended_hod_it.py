# Generated by Django 3.2.7 on 2024-06-03 08:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hardware', '0076_alter_requisition_recommended_hod_it'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisition',
            name='recommended_hod_it',
            field=models.ForeignKey(blank=True, default=19, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recommended_hod_it_requisition', to=settings.AUTH_USER_MODEL, verbose_name='Recommended HOD of IT'),
        ),
    ]
