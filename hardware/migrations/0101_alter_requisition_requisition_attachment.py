# Generated by Django 3.2.7 on 2024-12-10 15:10

from django.db import migrations, models
import hardware.models


class Migration(migrations.Migration):

    dependencies = [
        ('hardware', '0100_requisition_requisition_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisition',
            name='requisition_attachment',
            field=models.FileField(blank=True, null=True, upload_to=hardware.models.requisition_attachment_upload_path, verbose_name='Requisition Attachment'),
        ),
    ]
