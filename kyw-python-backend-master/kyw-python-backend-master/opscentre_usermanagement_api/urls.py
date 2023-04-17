from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('register',RegisterView.as_view()),
    path('login',LoginView.as_view()),
    path('user',UserView.as_view()),
    path('opsusers',OpsTeamView.as_view()),  
    path('opsusers/<str:opid>',OpsTeamById.as_view(), name ='OpsById'),    
    path('recruiters',Recruiters.as_view()),
    path('recruiters/<str:recid>',RecruitersById.as_view(), name ='RecById'),
    path('companies',Companies.as_view()),
    path('companies/<str:compid>',CompaniesById.as_view(), name ='CompById'),
    path('employees/<str:keyid>',Employees.as_view(), name='Employees'),
    path('candidates',Candidates.as_view()),
    path('candidates/<str:candid>',CandidatesById.as_view(), name ='CandidateById'),
    path('candprofiles/<str:keyid>',CandProfile.as_view(), name='CandProfile'),
    path('logout',LogoutView.as_view()),
  # path('auctions',Auctions.as_view()),
  # path('servicerqs',ServiceRqs.as_view()),
  # path('forgot',Forgotpassword.as_view())

    path('auctions',AuctionView.as_view()),
    path('auctions/<id>',CandidateAuctionView.as_view()),
    path('bids',BidView.as_view()),

    path('servicerqs', ServiceRqView.as_view()),
    path('servicerqs/<str:srid>', ServiceRqById.as_view()),
    path('servicerqs/srid/<str:rqid>', ServiceRqByRqId.as_view()),
    path('srcomments', SRComments.as_view()),
    path('dashboard', DashboardView.as_view()),
    path('dashboard/cache', DashboardCachedView.as_view()),



]