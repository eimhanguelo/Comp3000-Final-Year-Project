# Generated by Django 3.2.7 on 2024-12-23 13:43

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0027_auto_20241223_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eticket',
            name='problem_description',
            field=ckeditor.fields.RichTextField(default='No description'),
        ),
        migrations.AlterField(
            model_name='historicaleticket',
            name='problem_description',
            field=ckeditor.fields.RichTextField(default='No description'),
        ),
    ]
