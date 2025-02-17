# Generated by Django 3.2.7 on 2021-10-14 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('connectivity', '0033_auto_20211014_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lanrequestit',
            name='cable_tag',
        ),
        migrations.RemoveField(
            model_name='lanrequestit',
            name='computer_name',
        ),
        migrations.RemoveField(
            model_name='lanrequestit',
            name='cpu_model',
        ),
        migrations.RemoveField(
            model_name='lanrequestit',
            name='ip_address',
        ),
        migrations.RemoveField(
            model_name='lanrequestit',
            name='os',
        ),
        migrations.RemoveField(
            model_name='lanrequestit',
            name='printer_model',
        ),
        migrations.RemoveField(
            model_name='lanrequestit',
            name='scanner_model',
        ),
        migrations.RemoveField(
            model_name='lanrequestit',
            name='switch_name',
        ),
        migrations.RemoveField(
            model_name='lanrequestit',
            name='switch_port',
        ),
        migrations.RemoveField(
            model_name='lanrequestit',
            name='vlan',
        ),
        migrations.AddField(
            model_name='lanrequestit',
            name='required_ip_address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='connectivity.lan'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lanrequestit',
            name='lanrequest',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lanrequest_it', to='connectivity.lanrequest'),
        ),
    ]
