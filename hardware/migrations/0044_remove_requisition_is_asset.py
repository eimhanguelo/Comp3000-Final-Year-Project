# Generated by Django 3.2.7 on 2022-07-18 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0043_rename_signer_requisitionit_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requisition',
            name='is_asset',
        ),
    ]
