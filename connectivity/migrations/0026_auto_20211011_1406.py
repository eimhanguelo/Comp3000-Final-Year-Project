# Generated by Django 3.2.7 on 2021-10-11 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connectivity', '0025_auto_20211011_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lanrequestit',
            name='vlan',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Vlan',
        ),
    ]
