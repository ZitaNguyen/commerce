from http.client import FOUND
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Category, Listing, User, Watchlist, Bid, Comment
from .forms import ListingForm


def index(request):
    listings = Listing.objects.all().filter(active=True).order_by('id').reverse()
    return render(request, "auctions/index.html", {
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


@login_required
def create_listing(request):
    if request.method == "POST":
        listing_form = ListingForm(request.POST, request.FILES)

        if listing_form.is_valid():
            title = listing_form.cleaned_data['title']
            category = listing_form.cleaned_data['category']
            description = listing_form.cleaned_data['description']
            image = listing_form.cleaned_data['image']
            starting_bid = listing_form.cleaned_data['starting_bid']

            Listing.objects.create(
                user = request.user,
                category = category,
                title = title,
                description = description,
                image = image,
                starting_bid = starting_bid,
            )
            return HttpResponseRedirect(reverse("index"))

    else:
        listing_form = ListingForm()
        return render(request, "auctions/create_listing.html", {'listing_form': listing_form})


@login_required
def listing_page(request, listing_id):
    if request.user is None:
        return redirect('login')

    listing = Listing.objects.get(id=listing_id)
    try:
        user_watchlist = Watchlist.objects.get(user=request.user)
    except Watchlist.DoesNotExist:
        user_watchlist = None

    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "user_watchlist": user_watchlist
        })


def toggle_watchlist(request, listing_id):
    if request.method == "POST":
        current_listing = Listing.objects.get(id=listing_id)
        try:
            user_watchlist = Watchlist.objects.get(user=request.user)
        except Watchlist.DoesNotExist:
            user_watchlist = None

        if user_watchlist is None:
            user_watchlist = Watchlist.objects.create(user=request.user)
            user_watchlist.listings.add(current_listing)
            user_watchlist.save()

        elif current_listing not in user_watchlist.listings.all():
            user_watchlist.listings.add(current_listing)
            user_watchlist.save()

        else:
            user_watchlist.listings.remove(current_listing)
            user_watchlist.save()

        return redirect('listing_page', listing_id=listing_id)


@login_required
def watchlist(request):
    try:
        watchlist = Watchlist.objects.get(user=request.user)
    except Watchlist.DoesNotExist:
        watchlist = None

    if watchlist is None or not watchlist.listings.all():
        messages.info(request, 'Nothing has been added to watchlist.')
        return redirect('index')

    return render(request, "auctions/watchlist.html", {
        "listings": watchlist.listings.all()
    })


def place_bid(request, listing_id):
    if request.method == "POST":
        bid = request.POST["bid"]
        listing = Listing.objects.get(id=listing_id)

        # Check bid condition
        if not listing.current_bid and int(bid) < listing.starting_bid:
            messages.warning(request, 'Your bid is smaller than the starting bid')
            return redirect('listing_page', listing_id=listing_id)
        elif listing.current_bid and int(bid) <= listing.current_bid.bid:
            messages.warning(request, 'Your bid is equal or smaller than the current bid')
            return redirect('listing_page', listing_id=listing_id)

        current_bid = Bid.objects.create(
                        bidder = request.user,
                        listing = listing,
                        bid = bid
        )

        listing.bids.add(current_bid)
        listing.current_bid = current_bid
        listing.save()

        messages.success(request, 'You have successfully placed a bid for %s!' % listing.title)
        return redirect('listing_page', listing_id=listing_id)


def close_bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        listing.active = False
        listing.save(update_fields=['active'])

        messages.info(request, 'This listing has been closed.')
        return redirect('listing_page', listing_id=listing_id)


def add_comment(request, listing_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        listing = Listing.objects.get(id=listing_id)

        comment = Comment.objects.create(
                    commenter = request.user,
                    listing = listing,
                    comment = comment
        )

        listing.comments.add(comment)
        listing.save()

        messages.success(request, 'Your comment has been successfully added!')
        return redirect('listing_page', listing_id=listing_id)


@login_required
def category(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })


@login_required
def category_view(request, category_id):
    category = Category.objects.get(id=category_id)
    listings_of_same_category = Listing.objects.filter(category=category_id, active=True).order_by('id').reverse()

    if not listings_of_same_category:
        messages.info(request, 'No listing in %s category' % category.name)
        return redirect('category')

    return render(request, 'auctions/category_view.html', {
        "listings": listings_of_same_category,
        "category": category.name
    })