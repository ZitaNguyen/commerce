from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='listing_creator')
    title = models.CharField(max_length=64)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category')
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    starting_bid = models.IntegerField()
    bids = models.ManyToManyField('Bid', related_name='bids', blank=True)
    current_bid = models.ForeignKey('Bid', on_delete=models.CASCADE, related_name='current_bid', blank=True, null=True)
    active = models.BooleanField(default=True)
    comments = models.ManyToManyField('Comment', related_name='comments', blank=True)

    def __str__(self):
        return f"{self.title}"

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Bid(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='bidder')
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='listing_bidded')
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.listing, self.bid, self.user}"


class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='commenter')
    comment = models.TextField()

    def __str__(self):
        return f"{self.user, self.comment}"


class Watchlist(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_watchlist')
    listings = models.ManyToManyField('Listing', related_name='listings_in_watchlist', blank=True)

    def __str__(self):
        return f"{self.user}"