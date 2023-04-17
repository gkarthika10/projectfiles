from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('auction',AuctionView.as_view()),
    path('auction/<id>',CandidateAuctionView.as_view()),
    path('bids',BidView.as_view()),
    path('interview-auctions',EmployerInterviewAuctionView.as_view()),
    path('interview-auctions/<id>',EmployerOfferView.as_view()),
    path('offer',EmployerOfferView.as_view()),
    path('favourites',FavouritesView.as_view()),
    path('favourites/<id>',FavouritesView.as_view()),
    
]

