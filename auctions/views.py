from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, WatchList, Bid, Comment

from .forms import ListingForm, CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def index(request):
    listings = Listing.objects.all()
    context = {"listings": listings}
    return render(request, "auctions/index.html", context)


@login_required(login_url="login")
def listing_details(request, pk):
    listing = Listing.objects.get(id=pk)
    comments = Comment.objects.filter(listing=listing)
    context = {"listing": listing, "comments": comments}
    return render(request, "auctions/listing_detail.html", context)


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="login")
def CreateListings(request):
    form = ListingForm()
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(
                commit=False
            )  # Create a listing instance but don't save it yet
            listing.user = request.user
            listing.save()
            form.save()
            return redirect("index")
        else:
            form = ListingForm()
    return render(request, "auctions/create_listings.html", {"form": form})


@login_required(login_url="login")
def Watchlists(request):
    watchlists = WatchList.objects.all()
    context = {"watchlists": watchlists}
    return render(request, "auctions/watchlist.html", context)


@login_required(login_url="login")
def add_to_watchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = request.user

        # Check if the listing is already in the user's watchlist
        if not WatchList.objects.filter(user=user, listing=listing).exists():
            watchlist_entry = WatchList(user=user, listing=listing)
            watchlist_entry.save()
        return redirect("listing_details", pk=listing_id)


@login_required(login_url="login")
def Place_bid(request, listing_id):
    if request.method == "POST":
        bid_value = request.POST.get("bid_value")
        listing = Listing.objects.get(pk=listing_id)
        user = request.user

        # Check if the bid is greater than the starting bid
        if float(bid_value) >= listing.starting_bid:
            # Update the starting bid for the listing
            listing.winner = user
            listing.starting_bid = float(bid_value)
            listing.save()

            # Create or update the bid entry for the user and listing
            bid_entry, created = Bid.objects.get_or_create(listing=listing)
            listing.user = user
            bid_entry.bid = float(bid_value)
            bid_entry.save()
        else:
            messages.error(
                request,
                f"The bid value is small. Place a bid greater than or equals to {listing.starting_bid}",
                fail_silently=True,
            )
        return redirect("listing_details", pk=listing_id)


@login_required(login_url="login")
def close_auction(request, listing_id):
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=listing_id)

        if user == listing.user:
            listing.closed = True
            messages.warning(
                request,
                f"You closed  Auctions for the listing {listing.title}. And the winner is {listing.winner}",
            )

        return redirect("listing_details", pk=listing_id)


@login_required(login_url="login")
def CreateComment(request, listing_id):
    form = CommentForm()
    if request.method == "POST":
        user = request.user
        listing = Listing.objects.get(pk=listing_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.listing = listing
            comment.save()
            return redirect("index")
        else:
            form = CommentForm()
    return render(request, "auctions/comment.html", {"form": form})
