from django.urls import reverse
# Choices for the condition field in the Listing model
CONDITION_CHOICES = [
    ('new', 'Brand New'),
    ('opened', 'Opened'),
    ('used', 'Used'),
    ("not_working", 'Not working')
]


# Choices for the category field in the Listing model
CATEGORY_CHOICES = [
    ('electronics', 'Electronics'),
    ('fashion_and_clothes', 'Fashion & Clothes'),
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
    (None, 'Other'),
]


# Status of listing
STATUS_CHOICES = [
    ("active", 'Active'),
    ('inactive', 'Inactive'),
    ('closed', 'Closed'),
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
def check_highest_bid(listing, user):
    if listing.bids.exists():
        highest_bid = listing.bids.order_by('-price').first()
        return True if highest_bid.user.id == user.id else False
    else:
        return False


# Apply search
def do_search(request_get, listings):
    if "q" in request_get or "category" in request_get:
        # Get a search query
        search = request_get.get('q', "")
        # Get a selected category
        selected_category = request_get.get('category', "all")
        # Make search
        if search:
            listings = listings.filter(title__icontains = search)
        if selected_category != "all":
            listings = listings.filter(category = selected_category)
    else: 
        search = ''
        selected_category = None
    return listings, search, selected_category


# Create redirect url with search
def create_search_url(reverse_argument, request):
    
    # Get searched category
    selected_category = request.POST["category"]
    # Get search
    search = request.POST["search"].strip(" ")
    if not search or not selected_category:
        # Get searched category (for mobile search)
        selected_category = request.POST["category_mobile"]
        # Get search (for mobile search)
        search = request.POST["search_mobile"].strip(" ")
    
    url = reverse(reverse_argument)
    if search:
        url += f"?q={search}"
    if selected_category != "all":
        if "?" in url:
            url += f"&category={selected_category}"
        else:
            url += f"?category={selected_category}"
    return url