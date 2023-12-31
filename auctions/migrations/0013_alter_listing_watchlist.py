# Generated by Django 4.2.1 on 2023-07-01 14:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_listing_watchlist_delete_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watching_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
