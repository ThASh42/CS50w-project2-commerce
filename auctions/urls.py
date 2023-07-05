from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("watchlist", views.my_watchlist, name="my_watchlist"),
    path("category", views.category, name="category"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("create", views.create, name="create"),
    path("<int:listing_id>/comment", views.comment, name="comment"),
    
    path("<int:listing_id>/watchlist", views.watchlist, name="watchlist"),
    path("<int:listing_id>/delete-watchlist", views.delete_watchlist, name="delete_watchlist"),
    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
