from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("watchlist", views.my_watchlist, name="my_watchlist"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/watchlist", views.watchlist, name="watchlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
