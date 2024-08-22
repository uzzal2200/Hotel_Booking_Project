
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('details/<int:id>', DetailsPostView.as_view(), name= 'detail_post'),
    path('booking/<int:id>', Booking, name= 'booking'),
    path('edit_rating/<int:id>/<int:post_id>/', Edit_rating, name= 'edit_rating'),
    path('delete/<int:id>/<int:post_id>/', Delete_rating, name= 'delete'),
    path('cmt/edit/<int:id>/<int:post_id>/', Edit_cmt, name= 'edit_cmt'),
    path('cmt/delete/<int:id>/<int:post_id>/', Delete_cmt, name= 'delete_cmt'),

]
