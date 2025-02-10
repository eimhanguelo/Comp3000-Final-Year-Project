# Generated by Django 3.1.7 on 2021-04-04 17:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LanRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('justification', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recommended_hod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recommended_hod', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LanTransfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_ip_address', models.GenericIPAddressField()),
                ('transfer_location_plant', models.CharField(max_length=50)),
                ('transfer_location_old_IP', models.GenericIPAddressField(blank=True, null=True)),
                ('transfer_IT_equipment_list', models.TextField()),
                ('purpose_of_transfer', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recommended_hod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recommended_hod_lt', to=settings.AUTH_USER_MODEL)),
                ('recommended_hr', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recommended_hr_lt', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LanTransferSign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sign_type', models.CharField(choices=[('recommended_hod', 'Recommended by HOD'), ('recommended_hr', 'Approved by HR')], max_length=50)),
                ('date_signed', models.DateTimeField(auto_now_add=True)),
                ('lantransfer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lantransfer_sign', to='connectivity.lantransfer')),
                ('signer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LanTransferIT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provide_ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('vlan', models.IntegerField(default=0)),
                ('current_switch_name', models.CharField(max_length=30)),
                ('current_port', models.IntegerField(default=0)),
                ('required_switch_name', models.CharField(default='N/A', max_length=20)),
                ('required_port', models.IntegerField(default=0)),
                ('date_signed', models.DateTimeField(auto_now_add=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('lantransfer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lantransfer_it', to='connectivity.lantransfer')),
            ],
        ),
        migrations.CreateModel(
            name='LanRequestSign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sign_type', models.CharField(choices=[('confirmed', 'Confirm by HOD'), ('not_confirmed', 'Not Confirm by HOD')], default='Confirm by HOD', max_length=50)),
                ('date_signed', models.DateTimeField(auto_now_add=True)),
                ('lanrequest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lanrequest_sign', to='connectivity.lanrequest')),
                ('signer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LanRequestIT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('computer_name', models.CharField(blank=True, max_length=50, null=True)),
                ('os', models.CharField(blank=True, choices=[('win_10', 'Windows 10'), ('win_8.1', 'Windows 8.1'), ('win_8.0', 'Windows 8.1'), ('win_7', 'Windows 7')], max_length=15, null=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('vlan', models.IntegerField(default=0)),
                ('switch_name', models.CharField(max_length=30)),
                ('switch_port', models.IntegerField(blank=True, default=0, null=True)),
                ('cable_tag', models.CharField(blank=True, default='N/A', max_length=20, null=True)),
                ('cpu_model', models.CharField(blank=True, default='N/A', max_length=40, null=True)),
                ('printer_model', models.CharField(blank=True, default='N/A', max_length=20, null=True)),
                ('scanner_model', models.CharField(blank=True, default='N/A', max_length=20, null=True)),
                ('date_signed', models.DateTimeField(auto_now_add=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('lanrequest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lanrequest_it', to='connectivity.lanrequest')),
            ],
        ),
    ]
