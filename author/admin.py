from django.contrib import admin

from author.models import HotelBookingData, UserAccount, UserProfile
# Register your models here.

admin.site.register(UserAccount)
admin.site.register(HotelBookingData)
admin.site.register(UserProfile)