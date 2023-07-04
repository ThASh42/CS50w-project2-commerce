# Generated by Django 4.2.1 on 2023-07-04 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_alter_listing_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(blank=True, choices=[(None, 'No category'), ('electronics', 'Electronics'), ('fashion', 'Fashion'), ('home_and_garden', 'Home & Garden'), ('collectibles', 'Collectibles'), ('music_movies', 'Music & Movies'), ('books', 'Books'), ('sporting_goods', 'Sporting Goods'), ('automotive', 'Automotive'), ('toys_hobbies', 'Toys & Hobbies'), ('health_beauty', 'Health & Beauty'), ('home_appliances', 'Home Appliances'), ('jewelry_watches', 'Jewelry & Watches'), ('art_crafts', 'Art & Crafts'), ('baby_kids', 'Baby & Kids'), ('musical_instruments', 'Musical Instruments'), ('pet_supplies', 'Pet Supplies')], default=None, max_length=64, null=True),
        ),
    ]
