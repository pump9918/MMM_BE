# Generated by Django 4.1.7 on 2023-08-18 08:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_editorprofile_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_ID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile_user_ID', to=settings.AUTH_USER_MODEL),
        ),
    ]
