from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Listing(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_listings"
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField(default=0.0)
    starting_bid = models.IntegerField(default=1)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)
    winner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="winner", blank=True
    )
    image = models.ImageField(upload_to="images/", default=None, null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, default=None
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, null=True, blank=True, default=None
    )
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Bid(models.Model):
    user = models.ManyToManyField(User)
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, null=True, blank=True, default=None
    )
    bid = models.IntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.bid)

    def IsBidOkay(self):
        if self.bid > self.listing.starting_bid:
            return True
        else:
            return False


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} for {self.listing.title}"
