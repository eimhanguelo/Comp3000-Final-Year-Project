# Generated by Django 3.2.7 on 2022-03-06 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0034_auto_20220306_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalphone',
            name='switch_port',
            field=models.IntegerField(blank=True, null=True, verbose_name='Switch Port'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='switch_port',
            field=models.IntegerField(blank=True, null=True, verbose_name='Switch Port'),
        ),
    ]
