# Generated by Django 4.2.1 on 2023-07-01 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_time_creation_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='time',
            name='creation_time',
            field=models.DateField(auto_now=True),
        ),
    ]
