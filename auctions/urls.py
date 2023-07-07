from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("watchlist", views.my_watchlist, name="my_watchlist"),
    path("category", views.category, name="category"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/bid", views.bid, name="bid"),
    path("create", views.create, name="create"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    
    path("<int:listing_id>/close_auction", views.close_auction, name="close_auction"),
    path("<int:listing_id>/status", views.status, name="status"),
    path("my_listings", views.my_listings, name="my_listings"),
    
    path("<int:listing_id>/watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/delete-watchlist", views.delete_watchlist, name="delete_watchlist"),
    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
