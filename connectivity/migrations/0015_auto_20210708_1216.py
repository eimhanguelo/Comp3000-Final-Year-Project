# Generated by Django 3.1.7 on 2021-07-08 12:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connectivity', '0014_auto_20210706_1146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileaccess',
            name='dufiles_link',
        ),
        migrations.RemoveField(
            model_name='fileaccess',
            name='files_link',
        ),
        migrations.RemoveField(
            model_name='fileaccess',
            name='revoke_access_name',
        ),
    ]
