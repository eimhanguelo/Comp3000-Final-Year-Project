# Generated by Django 3.2.7 on 2024-06-27 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0041_alter_account_mail_activation'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='ext',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
