from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('register',RegisterView.as_view()),
    path('login',LoginView.as_view()),
    path('user',UserView.as_view()),
    path('logout', LogOutView.as_view()),
    path('forgot',Forgotpassword.as_view()),
    path('change-password/<token>/' , ChangePassword.as_view()),
    path('verify-mail/<token>/' , VerifyEmailView.as_view()),
    path('reverify-mail/' , VerifyEmailView.as_view()),
    path('register/<token>/',RegisterTeamView.as_view()),
    path('contact-us',ContactUs.as_view()),
]
