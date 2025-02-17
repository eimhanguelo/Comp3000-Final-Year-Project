# Generated by Django 3.2.7 on 2021-12-08 11:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('connectivity', '0042_alter_lanrequestsign_lanrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalLan',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(db_index=True)),
                ('computer_name', models.CharField(blank=True, db_index=True, max_length=50, null=True)),
                ('vlan', models.IntegerField(default=0)),
                ('switch_port', models.IntegerField(blank=True, default=0, null=True)),
                ('cable_tag', models.CharField(blank=True, default='N/A', max_length=20, null=True)),
                ('cpu_model', models.CharField(blank=True, default='N/A', max_length=40, null=True)),
                ('printer_model', models.CharField(blank=True, default='N/A', max_length=20, null=True)),
                ('scanner_model', models.CharField(blank=True, default='N/A', max_length=20, null=True)),
                ('remarks', models.TextField()),
                ('date_created', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('admin', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('os', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='connectivity.os')),
                ('switch_name', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='connectivity.switch')),
            ],
            options={
                'verbose_name': 'historical lan',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
