# Generated by Django 4.2.1 on 2023-06-30 13:51

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateField(auto_now=True)),
                ('creation_time', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='time',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='auctions.time'),
            preserve_default=False,
        ),
    ]
