from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing/<int:pk>", views.listing_details, name="listing_details"),
    path("create", views.CreateListings, name="create_listings"),
    path("create/comment/<int:listing_id>", views.CreateComment, name="create_comment"),
    path("All/WatchLists", views.Watchlists, name="watchlists"),
    path("watchList/<int:listing_id>", views.add_to_watchlist, name="watch_list"),
    path("place/bid/<int:listing_id>", views.Place_bid, name="place_bid"),
    path("close/auction/<int:listing_id>", views.close_auction, name="close_auction"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
