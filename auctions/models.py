from django.contrib.auth.models import AbstractUser
from django.db import models

from .utilities import CONDITION_CHOICES, CATEGORY_CHOICES

# * Bid class
class Bid(models.Model):
    bid = models.DecimalField(max_digits=5, decimal_places=2)
    time = models.DateTimeField()


# * Model of update and creation time
class Time(models.Model):
    update_time = models.DateField(auto_now=True)
    creation_time = models.DateField(auto_now=True)
    
    
    # provide "st", "nd", "rd" or "th"  suffix
    def provide_suffix(self, someday):
        return "th" if 11 <= someday <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(someday % 10, "th")
    
    
    # the function displays the creation time
    def print_creation_time(self):
        day = self.creation_time.day
        suffix = self.provide_suffix(day)
        return self.creation_time.strftime(f"%B %d{suffix}, %Y")
    
    
    # the function displays the update time
    def print_update_time(self):
        day = self.update_time.day
        suffix = self.provide_suffix(day)
        return self.update_time.strftime(f"%B %d{suffix}, %Y")
    
    
    def __str__(self):
        return f"Creation Time: {self.creation_time}, Update Time: {self.update_time}"


# * Model of conditions
class Condition(models.Model):
    choices = CONDITION_CHOICES
    name = models.CharField(max_length=64, choices=choices)
    
    def __str__(self):
        return dict(Condition.choices).get(self.name, self.name)


# * User model
class User(AbstractUser):
    pass


# * Comment model
class Comment(models.Model):
    commentator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentator")
    message = models.TextField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
    is_modified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{ self.commentator }, { self.time }"


# * Listing model
class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=200)
    bids = models.ManyToManyField(Bid, blank=True, related_name="bids")
    time = models.OneToOneField(Time, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, null=True, related_name='listings')
    category = models.CharField(max_length=64, default=None, null=True, blank=True, choices=CATEGORY_CHOICES)
    active_status = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watching_users")
    comments = models.ManyToManyField(Comment, blank=True, related_name="comments")
    
    
    def __str__(self):
        return self.title