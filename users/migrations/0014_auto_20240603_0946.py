# Generated by Django 3.2.7 on 2024-06-03 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0079_alter_requisition_recommended_hod_it'),
        ('users', '0013_auto_20240603_0927'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalprofile',
            old_name='is_hodit',
            new_name='is_hod_it',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='is_hodit',
            new_name='is_hod_it',
        ),
        migrations.DeleteModel(
            name='HOD_IT_Profile',
        ),
    ]
