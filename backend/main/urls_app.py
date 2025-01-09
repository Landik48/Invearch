from django.urls import path
from .views import *

urlpatterns = [
    path('users/user/', User.as_view()),
    path('users/auth/', auth),
    path('users/register/', register),
]