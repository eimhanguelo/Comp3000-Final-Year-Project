# Generated by Django 3.2.7 on 2021-10-07 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_accountsign_sign_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountit',
            name='mailbox_size',
        ),
    ]
