from django.db import models
from django.contrib.auth.models import User

from posts.models import Post



class HotelBookingData(models.Model):
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null= True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name = 'hotel_booking')
    price = models.DecimalField(max_digits=5, decimal_places=1, null = True, blank = True)
    image = models.ImageField(upload_to='posts/', null= True, blank=True)
    post = models.ForeignKey(Post, related_name = 'hotel_booking' , on_delete= models.CASCADE,  blank=True, null=True)
    
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    image = models.ImageField(upload_to='profile/', null=True, blank=True, )
    user = models.OneToOneField(User, related_name = 'user_profile', on_delete= models.CASCADE, blank=True, null=True)
    
class UserAccount(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=1, default=0)
    user = models.OneToOneField(User, on_delete= models.CASCADE, related_name = 'user_account',  blank=True, null=True,)