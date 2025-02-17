# Generated by Django 3.2.7 on 2022-07-17 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('connectivity', '0068_laninstrumentsign_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='InternetHOD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sign_type', models.CharField(choices=[('Agreed', 'Agreed'), ('Disagreed', 'Disagreed')], default='Agreed', max_length=50)),
                ('comment', models.CharField(blank=True, max_length=250, null=True)),
                ('date_signed', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='InternetHR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sign_type', models.CharField(choices=[('Agreed', 'Agreed'), ('Disagreed', 'Disagreed')], default='Agreed', max_length=50)),
                ('comment', models.CharField(blank=True, max_length=250, null=True)),
                ('date_signed', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='InternetIT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=250, null=True)),
                ('date_signed', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='internet',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.DeleteModel(
            name='InternetSign',
        ),
        migrations.AddField(
            model_name='internetit',
            name='internet',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='internet_it', to='connectivity.internet'),
        ),
        migrations.AddField(
            model_name='internethr',
            name='internet',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='internet_hr', to='connectivity.internet'),
        ),
        migrations.AddField(
            model_name='internethr',
            name='signer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='internethod',
            name='internet',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='internet_hod', to='connectivity.internet'),
        ),
        migrations.AddField(
            model_name='internethod',
            name='signer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
