# Generated by Django 3.2.7 on 2024-05-29 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0071_auto_20240228_2302'),
    ]

    operations = [
        migrations.AddField(
            model_name='requisition',
            name='new_asset_no',
            field=models.CharField(default='', max_length=100, verbose_name='New Asset No'),
        ),
    ]
