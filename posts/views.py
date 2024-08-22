
from django.urls import reverse
from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from author.models import HotelBookingData, UserAccount
from author.views import ConfarmationEmail
from posts.models import RatingModel
from .forms import *
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

    
class DetailsPostView(DetailView):
    model = Post
    pk_url_kwarg = 'id'
    template_name = 'post_details.html'
    
    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data = self.request.POST)
        rating_form = RatingForm(data = self.request.POST)
        post = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = self.request.user
            new_comment.save()
        if rating_form.is_valid():
            rating_form = rating_form.save(commit=False)
            rating_form.reviewer = self.request.user
            rating_form.post = post
            rating_form.save()
            
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any):
        context =  super().get_context_data(**kwargs)
        post = self.object 
        comments = post.comment.all()
        rating_data = RatingModel.objects.filter(post = post)
        comment_form = CommentForm()
        
        rating_form = RatingForm()
        
        if self.request.user.is_authenticated:
            rating_data = RatingModel.objects.filter(post = post)
            booking = HotelBookingData.objects.filter(author = self.request.user, post=post)
            context['rev'] = booking
            print(booking)
            if HotelBookingData.objects.filter(author = self.request.user, post = post):
                context['booked'] = True
            
        post = self.get_object()
        booked = False
        
        context['rating'] = rating_data
        context['comments'] = comments
        context['comment_form'] = comment_form
        context['rating_form'] = rating_form
       
        return context
    
    
    
@login_required
def Booking(request, id):
    try:
        if request.user.is_authenticated:
            acc = UserAccount.objects.get(user=request.user)
            post = Post.objects.get(id=id)
            if acc.balance >= post.price:
                acc.balance -= post.price
                acc.save()
                add_data = HotelBookingData.objects.create(
                    title =post.title,
                    address = post.address,
                    content=post.content,
                    price=post.price,
                    author=request.user,
                    image=post.image,
                    post = post,
                )
                add_data.save()
                messages.success(
                    request,
                    'Booking successfully'
                )
                mail_subject = 'Booking successfully'
                to_email = request.user.email
                ConfarmationEmail(request.user, to_email, "Booking", mail_subject, 0, 'booking_email.html')
            else:
                messages.error(
                    request,
                    "Your account doesn't have enough money."
                )
        else:
            return redirect('login')

    except (UserAccount.DoesNotExist, Post.DoesNotExist):
        messages.error(
            request,
            "Your account doesn't have enough money."
        )
    redirect_url = reverse('detail_post', args=[id])
    return redirect(redirect_url)


@login_required 
def Edit_rating(request, id, post_id):
    rating = RatingModel.objects.get(pk = id, reviewer = request.user )
    
    if request.method == 'POST':
        form = RatingForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            return redirect('detail_post', id=post_id)  
    else:
        form = RatingForm(instance=rating)
    return render(request, 'update.html', {'form': form})



def Delete_rating(request, id, post_id):
    RatingModel.objects.get(pk = id, reviewer = request.user ).delete()
    return redirect('detail_post', id=post_id)  


@login_required 
def Edit_cmt(request, id, post_id):
    cmt = Comment.objects.get(pk = id, user = request.user )
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance = cmt)
        if form.is_valid():
            form.save()
            return redirect('detail_post', id=post_id)  
    else:
        form = CommentForm(instance=cmt)
    return render(request, 'update.html', {'form': form})


@login_required 
def Delete_cmt(request, id, post_id):
    Comment.objects.get(pk = id, user = request.user ).delete()
    return redirect('detail_post', id=post_id)  
    
    
