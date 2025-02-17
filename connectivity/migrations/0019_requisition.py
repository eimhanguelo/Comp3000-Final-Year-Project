# Generated by Django 3.1.7 on 2021-07-28 14:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('connectivity', '0018_auto_20210726_0939'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requisition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('requisition_type', models.CharField(choices=[('new', 'New'), ('repair', 'Repair')], max_length=50)),
                ('requisition_no', models.CharField(max_length=100)),
                ('cost_center', models.CharField(max_length=100)),
                ('new_asset_no', models.CharField(max_length=100)),
                ('hms_No', models.CharField(max_length=100)),
                ('pr_no', models.CharField(max_length=100)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recommended_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recommended_by_requisition', to=settings.AUTH_USER_MODEL)),
                ('recommended_hod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recommended_hod_requisition', to=settings.AUTH_USER_MODEL)),
                ('recommended_hod_it', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recommended_hod_it_requisition', to=settings.AUTH_USER_MODEL)),
                ('recommended_hr', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recommended_hr_requisition', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
