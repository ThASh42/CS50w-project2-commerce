from django.contrib.auth.models import AbstractUser
from django.db import models

from .utilities import CONDITION_CHOICES, CATEGORY_CHOICES, STATUS_CHOICES


# * Model of update and creation time
class Time(models.Model):
    update_time = models.DateField(auto_now=True)
    creation_time = models.DateField(auto_now=True)

    def __str__(self):
        return f"Creation Date: {self.creation_time}, Update Date: {self.update_time}"


# * User model
class User(AbstractUser):
    pass


# * Comment model
class Comment(models.Model):
    commentator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commentator"
    )
    message = models.TextField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
    is_modified = models.BooleanField(default=False)

    def __str__(self):
        return f"{ self.commentator }, { self.time }"


# * Bid class
class Bid(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        return f"{ self.id }: User({ self.user.id }); price: { self.price }; Time: { self.time }"


# * Listing model
class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_bid = models.DecimalField(max_digits=20, decimal_places=2)
    image = models.URLField(max_length=256)
    bids = models.ManyToManyField(Bid, blank=True, related_name="bids")
    time = models.OneToOneField(Time, on_delete=models.SET_NULL, null=True)
    condition = models.CharField(
        max_length=16, null=True, choices=CONDITION_CHOICES
    )
    category = models.CharField(
        max_length=32, default=None, null=True, blank=True, choices=CATEGORY_CHOICES
    )
    active_status = models.CharField(
        max_length=16, default="active", choices=STATUS_CHOICES
    )
    watchlist = models.ManyToManyField(User, blank=True, related_name="watching_users")
    comments = models.ManyToManyField(Comment, blank=True, related_name="comments")
    winner = models.OneToOneField(
        User, on_delete=models.SET_NULL, blank=True, null=True, default=None
    )

    def __str__(self):
        return self.title


class UserBiddingActivity(models.Model):
    active_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="active_bidding_user")
    active_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="active_listing")
    
    def __str__(self):
        return f"{self.active_user} - {self.active_listing_id}"