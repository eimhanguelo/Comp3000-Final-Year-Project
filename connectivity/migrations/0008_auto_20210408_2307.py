# Generated by Django 3.1.7 on 2021-04-08 23:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connectivity', '0007_auto_20210408_2241'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fileaccess',
            old_name='recommended_hod_other_department',
            new_name='other_dept_head',
        ),
    ]
