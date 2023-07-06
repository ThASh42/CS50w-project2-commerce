from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .utilities import CONDITION_CHOICES, CATEGORY_CHOICES, get_price, check_user, check_price
from decimal import Decimal, InvalidOperation

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active_status=True)
    })


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


def status(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        if request.user.id == listing.owner.id:
            listing.active_status = not listing.active_status
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
        else:
            message = "You are not the owner of that listing"
            redirect_url = reverse("listing", args=(listing_id,)) + f'?message={ message }'
            return HttpResponseRedirect(redirect_url)


# Place bid
@login_required
def bid(request, listing_id):
    if request.method == "POST":
        
        bid_price = Decimal(request.POST["bid"])
        
        listing = Listing.objects.get(pk=listing_id)
        current_price = get_price(listing)
        
        user = request.user
        
        has_highest_bid = check_user(listing, user)
        
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


# Display listings by category
def category(request):
    if request.method == "GET":
        return render(request, "auctions/category.html", {
            "categories": CATEGORY_CHOICES,
        })
    elif request.method == "POST":
        
        selected_category = request.POST["category"]
        listings = Listing.objects.filter(category=selected_category, active_status=True)
        
        return render(request, "auctions/category.html", {
            "categories": CATEGORY_CHOICES,
            "selected_category": selected_category,
            "listings": listings,
        })


@login_required
def create(request):
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
        
        condition_name = request.POST["condition"]
        condition = Condition.objects.get(name = condition_name)
        
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
        )
        listing.save()
        
        return HttpResponseRedirect(reverse("index"))


@login_required
def watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user.id
        listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


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
