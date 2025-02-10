# Generated by Django 3.2.7 on 2022-07-14 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connectivity', '0066_auto_20220714_0808'),
    ]

    operations = [
        migrations.AddField(
            model_name='laninstrument',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='laninstrumentit',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='laninstrumentsign',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='laninstrumentsign',
            name='sign_type',
            field=models.CharField(choices=[('Agreed', 'Agreed'), ('Disagreed', 'Disagreed')], default='Agreed', max_length=15),
        ),
    ]
