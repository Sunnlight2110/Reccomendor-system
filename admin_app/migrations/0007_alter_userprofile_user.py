# Generated by Django 5.1.6 on 2025-03-05 07:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0006_user_age_user_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
