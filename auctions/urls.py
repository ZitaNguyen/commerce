from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing_page, name="listing_page"),
    path("listing/<int:listing_id>/toggle_watchlist", views.toggle_watchlist, name="toggle_watchlist"),
    path("listing/<int:listing_id>/place_bid", views.place_bid, name="place_bid"),
    path("listing/<int:listing_id>/close_bid", views.place_bid, name="close_bid"),
]
