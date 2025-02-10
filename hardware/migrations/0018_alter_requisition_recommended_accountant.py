# Generated by Django 3.2.7 on 2022-01-13 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hardware', '0017_auto_20220113_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisition',
            name='recommended_accountant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recommended_accountant_requistion', to=settings.AUTH_USER_MODEL, verbose_name='Recommended Accountant'),
        ),
    ]
