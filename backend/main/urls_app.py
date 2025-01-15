from django.urls import path
from .views import *

urlpatterns = [
    path('users/user/', User.as_view()),
    path('startups/', StartupsList.as_view()),
    path('users/auth/', auth),
    path('users/register/', register),
    path('startups/startup/<int:startupid>/', Startup.as_view()),
]