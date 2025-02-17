# Generated by Django 3.2.7 on 2021-10-13 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('connectivity', '0028_alter_lantransfersign_sign_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lantransferit',
            name='current_switch_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='current_switch_name_lt', to='connectivity.switch'),
        ),
        migrations.AlterField(
            model_name='lantransferit',
            name='required_switch_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='required_switch_name_lt', to='connectivity.switch'),
        ),
    ]
