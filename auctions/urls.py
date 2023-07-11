from django.urls import path

from . import views

urlpatterns = [
    # Listing paths
    path("", views.index, name="index"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/close_auction", views.close_auction, name="close_auction"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    path("<int:listing_id>/status", views.status, name="status"),
    path("<int:listing_id>/bids", views.bids, name="bids"),
    
    # Watchlist paths
    path("watchlist", views.my_watchlist, name="my_watchlist"),
    path("<int:listing_id>/watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/delete-watchlist", views.delete_watchlist, name="delete_watchlist"),
    
    # Edit paths
    path("<int:listing_id>/listing_edit", views.listing_edit, name="listing_edit"),
    
    # Other paths
    path("create-listing", views.listing_create, name="listing_create"),
    path("my_listings", views.my_listings, name="my_listings"),
    
    # User paths
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
