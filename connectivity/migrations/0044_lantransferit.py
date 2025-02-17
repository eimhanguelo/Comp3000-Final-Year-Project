# Generated by Django 3.2.7 on 2021-12-08 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('connectivity', '0043_historicallan'),
    ]

    operations = [
        migrations.CreateModel(
            name='LanTransferIT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=250)),
                ('date_signed', models.DateTimeField(auto_now_add=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('lantransfer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lantransfer_it', to='connectivity.lantransfer')),
            ],
        ),
    ]
