# Generated by Django 3.2.7 on 2024-06-19 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hardware', '0087_alter_requisition_recommended_hod_it'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requisition',
            name='new_asset_no',
        ),
        migrations.AddField(
            model_name='requisition',
            name='recommended_accountant',
            field=models.ManyToManyField(blank=True, related_name='recommended_accountant_requisitions', to=settings.AUTH_USER_MODEL, verbose_name='Recommended Accountant (if Required)'),
        ),
        migrations.AddField(
            model_name='requisition',
            name='recommended_verifier_it',
            field=models.ManyToManyField(blank=True, related_name='recommended_verifier_it_requisitions', to=settings.AUTH_USER_MODEL, verbose_name='Recommended Verifier of IT'),
        ),
        migrations.RemoveField(
            model_name='requisition',
            name='recommended_hr',
        ),
        migrations.AddField(
            model_name='requisition',
            name='recommended_hr',
            field=models.ManyToManyField(blank=True, related_name='recommended_hr_requisitions', to=settings.AUTH_USER_MODEL, verbose_name='Recommended HR (if Required)'),
        ),
        migrations.CreateModel(
            name='RequisitionACC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sign_type', models.CharField(choices=[('Agreed', 'Agreed'), ('Disagreed', 'Disagreed')], default='Agreed', max_length=50)),
                ('new_asset_no', models.CharField(default='', max_length=100, verbose_name='New Asset No')),
                ('comment', models.CharField(blank=True, max_length=250, null=True)),
                ('date_signed', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('requisition', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='requisition_acc', to='hardware.requisition')),
                ('signer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
