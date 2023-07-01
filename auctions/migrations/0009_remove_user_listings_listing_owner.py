# Generated by Django 4.2.1 on 2023-07-01 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_time_creation_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='listings',
        ),
        migrations.AddField(
            model_name='listing',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]