from django.urls import path
from .views import *

urlpatterns = [
    path('add-member', EmployerTeamView.as_view()),
    path('employer-team',EmployeeAdminView.as_view()),
    path('notification',NotificationView.as_view()),
    
]
