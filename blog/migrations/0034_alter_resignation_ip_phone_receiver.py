# Generated by Django 3.2.7 on 2022-07-19 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0033_auto_20220719_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resignation',
            name='ip_phone_receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ip_phone_receiver', to=settings.AUTH_USER_MODEL),
        ),
    ]
