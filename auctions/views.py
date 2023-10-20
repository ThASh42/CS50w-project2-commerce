from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .utilities import CONDITION_CHOICES, CATEGORY_CHOICES
from .utilities import get_price, check_highest_bid, check_price, do_search, create_search_url
from .models import *
from decimal import Decimal

# Display active listings
def index(request):
    if request.method == "GET":
        # Get active listings
        listings = Listing.objects.filter(active_status="active")
        # Apply search
        listings, search, selected_category = do_search(request.GET, listings)

        return render(request, "auctions/index.html", {
            "listings": listings,
            "categories": CATEGORY_CHOICES,
            "selected_category": selected_category,
            "search": search,
        })
    elif request.method == "POST": # Search result
        url = create_search_url("index", request)
        return HttpResponseRedirect(url)


# Display listing page
def listing(request, listing_id):
    if request.method == "GET":
        listing = Listing.objects.get(pk=listing_id)
        is_watching = request.user in listing.watchlist.all()
        
        # Check if the current user is the owner of the listing
        owner_id = listing.owner.id
        is_owner = True if request.user.id == owner_id else False
        
        # Get comments
        comments = listing.comments.all()
        
        # Get current price
        current_price = get_price(listing)
        
        # Get name of category
        for category_tuple in CATEGORY_CHOICES:
            if category_tuple[0] == listing.category:
                category = category_tuple[1]
                break
        
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "is_watching": is_watching,
            "comments": comments,
            "is_owner": is_owner,
            "current_price": current_price,
            "category": category,
        })


# Edit listing
@login_required
def listing_edit(request, listing_id):
    
    listing = Listing.objects.get(pk=listing_id)
    
    # Check if the user is the owner of the listing
    if listing.owner != request.user:
        # Display an error message indicating an access error
        messages.error(request, "You cannot change a listing which is not yours")
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
    if request.method == "GET":
        return render(request, "auctions/listing_edit.html", {
            "conditions": CONDITION_CHOICES,
            "categories": CATEGORY_CHOICES,
            "listing": listing,
        })
    
    if request.method == "POST":
        # Update listing data
        if not listing.bids.exists(): # if bids exists, description can be only changed
            title = request.POST["title"]
            listing.title = title
            start_bid = request.POST["start-bid"]
            listing.start_bid = start_bid
            image_url = request.POST["image-url"]
            listing.image_url = image_url
            condition = request.POST["condition"]
            listing.condition = condition
            category = request.POST["category"]
            listing.category = category
        description = request.POST["description"]
        listing.description = description
        
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


# Edit comment page
@login_required
def comment_edit(request, listing_id, comment_id):
    
    # Get listing
    listing = Listing.objects.get(pk=listing_id)
    # Get comment
    comment = listing.comments.get(pk=comment_id)
    
    # Check if the user is the owner of the comment
    if comment.commentator != request.user:
        # Display an error message indicating an access error
        messages.error(request, "You are not owner of this comment")
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    
    if request.method == "GET":
        # Render comment edit page
        return render(request, "auctions/comment_edit.html", {
            "comment": comment,
            "listing_id": listing.id,
        })
    
    elif request.method == "POST":        
        # Change message
        new_message = request.POST["new-message"]
        if comment.message.strip() != new_message.strip():
            comment.message = new_message
            # Set is_modified = True
            comment.is_modified = True
            comment.save()
        
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


# Change status of listing
@login_required
def status(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        if not listing.bids.exists():
            listing = Listing.objects.get(pk=listing_id)
            if listing.active_status == "active":
                listing.active_status = "inactive"
            elif listing.active_status == "inactive":
                listing.active_status = "active"
            
            listing.save()
        else:
            messages.error(request, "You can't change your status due to existing bids")
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


# Close auction
@login_required
def close_auction(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        if listing.bids.exists():
            highest_bid = listing.bids.order_by('-price').first()
            listing.winner = highest_bid.user
            listing.active_status = "closed"
        else:
            messages.error(request, "There are no bidders for this listing")
        
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


# Page of bids
def bids(request, listing_id):
    if request.method == "GET":
        listing = Listing.objects.get(pk=listing_id)
        
        # Get all bids ordered by descending price
        bids = listing.bids.all().order_by('-price')
        
        return render(request, "auctions/bids.html", {
            "bids": bids,
            "listing": listing,
            "bidders": listing.bids.values('user').distinct().count(),
        })


# Display your own listings
@login_required
def my_listings(request):
    if request.method == "GET":
        # Get active listings
        listings = Listing.objects.filter(owner = request.user)
        # Search
        listings, search, selected_category = do_search(request.GET, listings)

        return render(request, "auctions/my_listings.html", {
            "listings": listings,
            "categories": CATEGORY_CHOICES,
            "search": search,
            "selected_category": selected_category,
        })
    elif request.method == "POST":
        url = create_search_url("my_listings", request)
        return HttpResponseRedirect(url)


# Page of all listings with user's bids
@login_required
def my_bids(request):
    if request.method == "GET":
        # Get all listings' ID
        ids = UserBiddingActivity.objects.filter(active_user__id=request.user.id).values_list('active_listing', flat=True)
        # Get all listings
        listings = Listing.objects.filter(id__in=ids)
        # Search
        listings, search, selected_category = do_search(request.GET, listings)

        return render(request, "auctions/my_bids.html", {
            "listings": listings,
            "categories": CATEGORY_CHOICES,
            "search": search,
            "selected_category": selected_category,
        })
    elif request.method == "POST":
        url = create_search_url("my_bids", request)
        return HttpResponseRedirect(url)


# Place bid
@login_required
def bid(request, listing_id):
    if request.method == "POST":
        
        bid_price = Decimal(request.POST["bid"])
        
        listing = Listing.objects.get(pk=listing_id)
        
        user = request.user
        
        has_highest_bid = check_highest_bid(listing, user)
        
        is_price_bigger = check_price(listing, bid_price)
        
        if not has_highest_bid and is_price_bigger:
            bid = Bid(
                price = bid_price,
                user = user,
            )
            bid.save()
            
            listing.bids.add(bid)
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        else:
            if has_highest_bid:
                messages.success(request, "Your bid is already the highest")
            else:
                messages.success(request, "Your bid price is not suitable")
            
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


# Create listing
@login_required
def listing_create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "conditions": CONDITION_CHOICES,
            "categories": CATEGORY_CHOICES,
        })
    if request.method == "POST":
        # Get the input data
        title = request.POST["title"]
        start_bid = request.POST["start-bid"]
        image_url = request.POST["image-url"]
        description = request.POST["description"]
        condition = request.POST["condition"]
        category = request.POST["category"]
        
        user = request.user
        # Create listing
        listing = Listing(
            owner = user,
            title = title,
            description = description,
            start_bid = start_bid,
            image = image_url,
            condition = condition,
            category = category,
        )
        listing.save()
        
        return HttpResponseRedirect(reverse("index"))


# Add listing to watchlist
@login_required
def add_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user.id
        listing.watchlist.add(user)
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


# Delete listing from watchlist
@login_required
def delete_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user.id
        listing.watchlist.remove(user)
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


# User's watchlist page
@login_required
def watchlist(request):
    if request.method == "GET":
        user_id = request.user.id
        listings = Listing.objects.filter(watchlist__id=user_id)
        # Search
        listings, search, selected_category = do_search(request.GET, listings)

        return render(request, "auctions/watchlist.html", {
            "listings": listings,
            "categories": CATEGORY_CHOICES,
            "selected_category": selected_category,
            "search": search,
        })
    if request.method == "POST":
        url = create_search_url("watchlist", request)
        return HttpResponseRedirect(url)



# Add comment to the listing
@login_required
def comment(request, listing_id):
    if request.method == "POST":
        
        # Get the input data
        user = request.user
        user_comment = request.POST["message"]
        
        if user_comment:
            comment = Comment(
                commentator = user,
                message = user_comment,
            )
            comment.save()
            
            listing = Listing.objects.get(pk=listing_id)
            listing.comments.add(comment)
        else:
            messages.error(request, "The comment must have content")
        
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


# Login
def login_view(request):
    if request.method == "POST":
        
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


# Logout
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Register
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
