# Generated by Django 3.2.7 on 2022-08-18 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Roster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'IT Duty Roster Plan',
            },
        ),
        migrations.CreateModel(
            name='ShiftPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sat', multiselectfield.db.fields.MultiSelectField(choices=[('G', 'G'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('On-Call', 'On-Call')], max_length=20)),
                ('sun', multiselectfield.db.fields.MultiSelectField(choices=[('G', 'G'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('On-Call', 'On-Call')], max_length=20)),
                ('mon', multiselectfield.db.fields.MultiSelectField(choices=[('G', 'G'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('On-Call', 'On-Call')], max_length=20)),
                ('tue', multiselectfield.db.fields.MultiSelectField(choices=[('G', 'G'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('On-Call', 'On-Call')], max_length=20)),
                ('wed', multiselectfield.db.fields.MultiSelectField(choices=[('G', 'G'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('On-Call', 'On-Call')], max_length=20)),
                ('thu', multiselectfield.db.fields.MultiSelectField(choices=[('G', 'G'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('On-Call', 'On-Call')], max_length=20)),
                ('fri', multiselectfield.db.fields.MultiSelectField(choices=[('G', 'G'), ('A', 'A'), ('B', 'B'), ('C', 'C'), ('On-Call', 'On-Call')], max_length=20)),
                ('engineer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shift_engineer', to=settings.AUTH_USER_MODEL)),
                ('roster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roster', to='informatix.roster')),
            ],
        ),
    ]
