from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *
from .utilities import CONDITION_CHOICES

def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(active_status=True)
    })


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user_id = request.user.id
    is_watching = request.user in listing.watchlist.all()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_watching": is_watching,
    })


def create(request):
    if request.method == "GET":
        return render(request, "auctions/create.html", {
            "conditions": CONDITION_CHOICES,
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


def watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user.id
        listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))



def delete_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user.id
        listing.watchlist.remove(user)
        return HttpResponseRedirect(reverse("listing", args=(listing_id,)))


def my_watchlist(request):
    user_id = request.user.id
    listings = Listing.objects.filter(watchlist__id=user_id)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


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
