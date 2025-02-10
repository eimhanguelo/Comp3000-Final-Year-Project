# Generated by Django 3.2.7 on 2022-08-17 16:24

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hardware', '0046_auto_20220817_1601'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalInventory',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('details', models.CharField(blank=True, max_length=254, null=True, verbose_name='Product Details')),
                ('remarks', models.CharField(blank=True, max_length=254, null=True)),
                ('product_condition', models.CharField(choices=[('Requisition Raised', 'Requisition Raised'), ('Sent to CHQ', 'Sent to CHQ'), ('In Stock', 'In Stock'), ('Delivery', 'Delivery')], default='Requisition Raised', max_length=50, verbose_name='Product Condition')),
                ('chalan', models.CharField(blank=True, max_length=100, null=True, verbose_name='Chalan No')),
                ('rqn_no', models.CharField(blank=True, max_length=100, null=True, verbose_name='RQN No')),
                ('chalan_copy', models.TextField(blank=True, max_length=100, null=True, verbose_name='Chalan Hard Copy')),
                ('date_created', models.DateTimeField(blank=True, editable=False)),
                ('date_updated', models.DateTimeField(blank=True, editable=False)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('creator', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('model', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='hardware.productmodel')),
                ('product', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='hardware.product')),
                ('requisition', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='hardware.requisition')),
                ('unit_type', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='hardware.quantityunit', verbose_name='Unit Type')),
                ('used_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical inventory',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
