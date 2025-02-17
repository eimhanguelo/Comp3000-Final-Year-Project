# Generated by Django 3.1.7 on 2021-04-07 19:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('connectivity', '0003_auto_20210407_1820'),
    ]

    operations = [
        migrations.CreateModel(
            name='Internet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('justification', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recommended_hod', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recommended_hod_ia', to=settings.AUTH_USER_MODEL)),
                ('recommended_hr', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recommended_hr_ia', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InternetSign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sign_type', models.CharField(choices=[('confirmed_hod', 'Recommended by HOD'), ('confirmed_hr', 'Approved By HR'), ('confirmed_it', 'Confirmed By IT Admin')], default='Recommended by HOD', max_length=50)),
                ('date_signed', models.DateTimeField(auto_now_add=True)),
                ('internet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='internet_sign', to='connectivity.internet')),
                ('signer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
