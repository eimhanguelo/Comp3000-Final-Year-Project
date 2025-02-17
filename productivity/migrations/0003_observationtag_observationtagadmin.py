# Generated by Django 3.2.7 on 2022-07-17 08:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('productivity', '0002_alter_opportunitytag_attachment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ObservationTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=253)),
                ('description', models.TextField()),
                ('observation_date', models.DateTimeField()),
                ('attachment', models.FileField(blank=True, null=True, upload_to='productivity')),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observation_tag_author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ObservationTagAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('On Review', 'On Review'), ('Informed Responsible Person', 'Informed Responsible Person'), ('Observation Resolved', 'Observation Resolved')], max_length=100)),
                ('comments', models.TextField()),
                ('date_signed', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('observation_tag', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='observation_tag', to='productivity.observationtag')),
            ],
        ),
    ]
