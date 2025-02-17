# Generated by Django 3.2.7 on 2024-11-30 08:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0018_alter_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='HODAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.department')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.location')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hod_access', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'department', 'location')},
            },
        ),
    ]
