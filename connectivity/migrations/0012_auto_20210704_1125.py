# Generated by Django 3.1.7 on 2021-07-04 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connectivity', '0011_fileaccess_location_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileaccess',
            name='location_link',
        ),
        migrations.AddField(
            model_name='fileaccess',
            name='files_link',
            field=models.CharField(default='N/A', max_length=230),
            preserve_default=False,
        ),
    ]
