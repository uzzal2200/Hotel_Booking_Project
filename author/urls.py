from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register_user, name = 'register'), 
    path('register_info/253/', RegisterInfo, name = 'register_info'), 
    path('login/', userLoginView.as_view(), name = 'login'), 
    path('logout/', UserLogout, name = 'logout'), 
    path('profile/', profile, name = 'profile'), 
    path('profile/edit', edit_profile, name = 'edit_profile'), 
    path('password_change/', password_change, name = 'password_change'), 
    path('deposit/', Deposit, name = 'deposit'), 
    path('00/hotel/leave/<int:id>/', HotelLeave, name = 'hotel_leave'),
    path('active/<uid64>/<token>/', activate, name = 'activate'), 
    
]