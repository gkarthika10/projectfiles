from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('profile',CandidateProfileView.as_view()),
    path('auction',CandidateAuctionView.as_view()),
    path('offer',CandidateAcceptOffer.as_view()),
    path('auction-availability',CandidateAvailabilityView.as_view())
   
]

