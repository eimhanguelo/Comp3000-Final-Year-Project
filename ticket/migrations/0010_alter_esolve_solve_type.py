# Generated by Django 3.2.7 on 2022-07-21 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0009_einternal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='esolve',
            name='solve_type',
            field=models.CharField(choices=[('solved', 'Solved'), ('closed', 'Closed')], default='Solved', max_length=20),
        ),
    ]
