# Choices for the condition field in the Listing model
CONDITION_CHOICES = [
    ('new', 'Brand New'),
    ('opened', 'Opened'),
    ('used', 'Used'),
    ("not_working", 'Not working')
]


# Choices for the category field in the Listing model
CATEGORY_CHOICES = [
    (None, 'No category'),
    ('electronics', 'Electronics'),
    ('fashion', 'Fashion'),
    ('home_and_garden', 'Home & Garden'),
    ('collectibles', 'Collectibles'),
    ('music_movies', 'Music & Movies'),
    ('books', 'Books'),
    ('sporting_goods', 'Sporting Goods'),
    ('automotive', 'Automotive'),
    ('toys_hobbies', 'Toys & Hobbies'),
    ('health_beauty', 'Health & Beauty'),
    ('home_appliances', 'Home Appliances'),
    ('jewelry_watches', 'Jewelry & Watches'),
    ('art_crafts', 'Art & Crafts'),
    ('baby_kids', 'Baby & Kids'),
    ('musical_instruments', 'Musical Instruments'),
    ('pet_supplies', 'Pet Supplies'),
]


# Get current price
def get_price(listing):
    if listing.bids.exists():
        bid = listing.bids.order_by('-price').first()
        return bid.price
    else:
        return listing.start_bid


# Check if the bid price is higher than the highest current price
# or if the bid price is higher or equal to the starter price
def check_price(listing, bid_price):
    if listing.bids.exists():
        highest_bid = listing.bids.order_by('-price').first()
        return bid_price > highest_bid.price
    else:
        return bid_price >= listing.start_bid


# Check if the user already has the highest bid
def check_user(listing, user):
    if listing.bids.exists():
        highest_bid = listing.bids.order_by('-price').first()
        return True if highest_bid.user.id == user.id else False
    else:
        return False
