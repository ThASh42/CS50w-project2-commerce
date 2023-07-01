from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class Bid(models.Model):
    bid = models.DecimalField(max_digits=5, decimal_places=2)
    time = models.DateTimeField()


class Time(models.Model):
    update_time = models.DateField(auto_now=True)
    creation_time = models.DateField(auto_now=True)
    
    
    def provide_suffix(self, someday):
        return "th" if 11 <= someday <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(someday % 10, "th")
    
    
    def print_creation_time(self):
        day = self.creation_time.day
        suffix = self.provide_suffix(day)
        return self.creation_time.strftime(f"%B %d{suffix}, %Y")
    
    
    def print_update_time(self):
        day = self.update_time.day
        suffix = self.provide_suffix(day)
        return self.update_time.strftime(f"%B %d{suffix}, %Y")
    
    
    def __str__(self):
        return f"Creation Time: {self.creation_time}, Update Time: {self.update_time}"


class Condition(models.Model):
    CONDITION_CHOICES = [
        ('new', 'Brand New'),
        ('opened', 'Opened'),
        ('used', 'Used'),
        ("not_working", 'Not working')
    ]
    
    name = models.CharField(max_length=64, choices=CONDITION_CHOICES)
    
    def __str__(self):
        return dict(Condition.CONDITION_CHOICES).get(self.name, self.name)


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length=200)
    bids = models.ManyToManyField(Bid, blank=True, related_name="bids")
    time = models.OneToOneField(Time, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.SET_NULL, null=True, related_name='listings')
    
    
    def print_listing(self):
        bid_plural = "bids" if self.bids.count() != 1 else "bid"
        return f"""{self.title} <br> 
        <strong> US ${self.start_bid} </strong> <br>
        {self.bids.count()} {bid_plural}
        """
    
    
    def __str__(self):
        return self.title


class User(AbstractUser):
    listings = models.ManyToManyField(Listing, blank=True, related_name="listings")
    pass
