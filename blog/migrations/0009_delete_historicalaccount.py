# Generated by Django 3.2.7 on 2021-10-16 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_historicalaccount'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HistoricalAccount',
        ),
    ]
