# Generated by Django 4.2.1 on 2023-07-06 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_comment_delete_comments_alter_listing_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bid',
            name='time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
