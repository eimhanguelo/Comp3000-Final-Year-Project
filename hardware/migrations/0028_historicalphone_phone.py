# Generated by Django 3.2.7 on 2022-03-05 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('connectivity', '0063_alter_lanrequestsign_sign_type'),
        ('hardware', '0027_alter_requisition_cost_center'),
    ]

    operations = [
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac_address', models.CharField(max_length=100, unique=True, verbose_name='MAC Address')),
                ('ext', models.CharField(blank=True, max_length=4, null=True, verbose_name='EXT')),
                ('model', models.CharField(blank=True, max_length=40, null=True, verbose_name='Model')),
                ('power_adapter', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=50, null=True, verbose_name='Power Adapter')),
                ('display_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Display Name')),
                ('phone_condition', models.CharField(choices=[('Reserved', 'Reserved'), ('Live', 'Live'), ('Repair', 'Repair'), ('Decommission', 'Decommission')], default='Reserved', max_length=50, verbose_name='Phone Condition')),
                ('remarks', models.CharField(blank=True, max_length=250, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='phone_creator', to=settings.AUTH_USER_MODEL)),
                ('provided_ip', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='connectivity.lan', verbose_name='Provided IP')),
            ],
            options={
                'verbose_name_plural': 'CISCO Phone Inventory List',
            },
        ),
        migrations.CreateModel(
            name='HistoricalPhone',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('mac_address', models.CharField(db_index=True, max_length=100, verbose_name='MAC Address')),
                ('ext', models.CharField(blank=True, max_length=4, null=True, verbose_name='EXT')),
                ('model', models.CharField(blank=True, max_length=40, null=True, verbose_name='Model')),
                ('power_adapter', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=50, null=True, verbose_name='Power Adapter')),
                ('display_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Display Name')),
                ('phone_condition', models.CharField(choices=[('Reserved', 'Reserved'), ('Live', 'Live'), ('Repair', 'Repair'), ('Decommission', 'Decommission')], default='Reserved', max_length=50, verbose_name='Phone Condition')),
                ('remarks', models.CharField(blank=True, max_length=250, null=True)),
                ('date_created', models.DateTimeField(blank=True, editable=False)),
                ('date_updated', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('creator', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('provided_ip', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='connectivity.lan', verbose_name='Provided IP')),
            ],
            options={
                'verbose_name': 'historical phone',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
