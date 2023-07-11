from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .utilities import CONDITION_CHOICES, CATEGORY_CHOICES
from .utilities import get_price, check_highest_bid, check_price
from .models import *
from decimal import Decimal


# Display active listings
def index(request):
    if request.method == "GET":
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.filter(active_status="active"),
            "categories": CATEGORY_CHOICES,
        })
    elif request.method == "POST": # Search result
        category = request.POST["category"]
        search = request.POST["search"]
        if not category == "all" or not search == "":
            
            if category == "all":
                listings = Listing.objects.filter(active_status="active", title__icontains=search)
            else:
                listings = Listing.objects.filter(active_status="active", category=category, title__icontains=search)
            
            return render(request, "auctions/index.html", {
                "listings": listings,
                "categories": CATEGORY_CHOICES,
                "selected_category": category
            })
        else:
            return HttpResponseRedirect(reverse("index"))


# Display listing page
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    is_watching = request.user in listing.watchlist.all()
    
    # Check if the current user is the owner of the listing
    owner_id = listing.owner.id
    is_owner = True if request.user.id == owner_id else False
    
    comments = listing.comments.all()
    
    current_price = get_price(listing)
    
    message = request.GET.get('message')
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_watching": is_watching,
        "comments": comments,
        "is_owner": is_owner,
        "current_price": current_price,
        "message": message,
    })


# Edit listing
@login_required
def listing_edit(request, listing_id):
    
    listing = Listing.objects.get(pk=listing_id)
    
    # Check if the logged-in user is the owner of the listing
    if listing.owner != request.user:
        # Display an error message indicating unauthorized access
        return HttpResponse("You are not authorized to edit this listing.")
    
    if request.method == "GET":
        
        return render(request, "auctions/listing_edit.html", {
            "conditions": CONDITION_CHOICES,
            "categories": CATEGORY_CHOICES,
            "listing": listing,
        })
    if request.method == "POST":
        
        # Update listing data
        title = request.POST["title"]
        listing.title = title
        if "start-bid" in request:
            start_bid = request.POST["start-bid"]
            listing.start_bid = start_bid
        description = request.POST["description"]
        listing.description = description
        image_url = request.POST["image-url"]
        listing.image_url = image_url
        condition = request.POST["condition"]
        listing.condition = condition
        category = request.POST["category"]
        listing.category = category
        
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


@login_required
def comment_edit(request, listing_id, comment_id):
    
    # Get listing
    listing = Listing.objects.get(pk=listing_id)
    # Get comment
    comment = listing.comments.get(pk=comment_id)
    
    
    # Check if the logged-in user is the owner of the comment
    if comment.commentator != request.user:
        # Display an error message indicating unauthorized access
        return HttpResponse("You are not authorized to edit this comment.")
    
    if request.method == "GET":
        return render(request, "auctions/comment_edit.html", {
            "comment": comment,
            "listing_id": listing.id,
        })
    elif request.method == "POST":
        
        # Change message
        new_message = request.POST["new-message"]
        comment.message = new_message
        comment.save()
        
        # Set is_modified True
        comment.is_modified = True
        
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


# Change status of listing
@login_required
def status(request, listing_id):
    if request.method == "POST":
        
        listing = Listing.objects.get(pk=listing_id)
        if listing.active_status == "active":
            listing.active_status = "inactive"
        elif listing.active_status == "inactive":
            listing.active_status = "active"
        
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


# Close auction
@login_required
def close_auction(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        
        highest_bid = listing.bids.order_by('-price').first()
        listing.winner = highest_bid.user
        listing.active_status = "closed"
        
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


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
        listings = Listing.objects.filter(owner = request.user)
        return render(request, "auctions/my.html", {
                "listings": listings
            })


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
            
            time = Time()
            time.save()
            
            bid = Bid(
                price = bid_price,
                time = time,
                user = user,
            )
            bid.save()
            
            listing.bids.add(bid)
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        else:
            if has_highest_bid:
                message = "Your bid is already the highest"
            else:
                message = "Your bid price is not suitable"
            redirect_url = reverse("listing", args=(listing_id,)) + f'?message={message}'
            return HttpResponseRedirect(redirect_url)


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
        
        time = Time()
        time.save()
        
        user = request.user
        # Create listing
        listing = Listing(
            owner = user,
            title = title,
            description = description,
            start_bid = start_bid,
            image = image_url,
            condition = condition,
            time = time,
            category = category,
        )
        listing.save()
        
        return HttpResponseRedirect(reverse("index"))


# Add listing to watchlist
@login_required
def watchlist(request, listing_id):
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


@login_required
def my_watchlist(request):
    user_id = request.user.id
    listings = Listing.objects.filter(watchlist__id=user_id)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


# Add comment to the listing
@login_required
def comment(request, listing_id):
    if request.method == "POST":
        
        # Get the input data
        user = request.user
        user_comment = request.POST["message"]
        
        comment = Comment(
            commentator = user,
            message = user_comment,
        )
        comment.save()
        
        listing = Listing.objects.get(pk=listing_id)
        listing.comments.add(comment)
        
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
