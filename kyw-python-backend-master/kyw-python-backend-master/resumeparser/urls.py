from django.contrib import admin
from django.urls import path,include
from .views import ParseResume
urlpatterns = [

    path("parser",ParseResume.as_view())
  
    
]

