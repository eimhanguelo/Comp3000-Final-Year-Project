# Generated by Django 3.2.7 on 2022-02-15 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0020_costcenter'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisition',
            name='cost_center_fk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hardware.costcenter', verbose_name='Cost Center FK'),
        ),
    ]
