# Generated by Django 3.2.7 on 2024-12-14 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connectivity', '0098_alter_os_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='centralprocessingunit',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='printermodel',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='scannermodel',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='switch',
            options={'ordering': ['id']},
        ),
    ]
