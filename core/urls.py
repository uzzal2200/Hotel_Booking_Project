from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomePage, name='home_page'),
    path('about/', AboutPage, name='about'),
    path('contact/', ContactPage, name='contact'),
]