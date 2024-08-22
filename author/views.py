
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.urls import reverse_lazy
from author.models import HotelBookingData, UserAccount, UserProfile
from .forms import *
from posts.models import Post
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes




def ConfarmationEmail(user, to_user, type, subject, amount, template):
        mail_subject = subject
        email_massage = render_to_string(template, 
        {
            'subject': subject,
            'type': type,
            'user': user,             
            'amount': amount,
            'datetime': timezone.now()
        })
        send_email = EmailMultiAlternatives(mail_subject, "", to = [to_user])
        send_email.attach_alternative(email_massage, "text/html")
        send_email.send()




def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            account = UserAccount.objects.create(balance = 0, user = user)
            account.save()
            
            profile = UserProfile.objects.create(
                image = form.cleaned_data['image'], 
                user = user
                )
            profile.save()
            
            messages.success(request, 'Account registration successful')
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"https://bookvista.onrender.com/author/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_reg_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            
            return redirect('register_info')
    else:
        form = RegisterForm()
    return render(request, 'user_form.html', {'form': form, 'type': 'Register'})


def RegisterInfo(request):
    return render(request, 'register_info.html')

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('profile')
    else:
        return redirect('register')


class userLoginView(LoginView):
    template_name = 'user_form.html'
   
    def get_success_url(self):
        return reverse_lazy('profile')
    
    def form_valid(self, form):
        messages.success(self.request, 'Login successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Loggged in information incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context

    
@login_required
def UserLogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home_page')


@login_required
def profile(request):
    user_data = request.user
    data = HotelBookingData.objects.filter(author=request.user)
    # image editing
    image_form = ChangeProfileImage()

    # Image editing
    if request.method == 'POST':
        image_form = ChangeProfileImage(request.POST, request.FILES, instance=request.user.user_profile)
        if image_form.is_valid():
            image_form.save()

    return render(request, 'profile.html', {'data': data, 'user_data': user_data, 'edit_image': image_form })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ChangeUserData(request.POST, instance = request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Profile Updated Successfully ')
            return redirect('profile')
        
    else:
        form = ChangeUserData(instance = request.user)
    return render(request, 'edit_profile.html', {'form': form})




@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password Updated successful')
            update_session_auth_hash(request, form.user)
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'pass_change.html', {'form': form})


# @login_required
# def Deposit (request):
#     if request.method == 'POST':
#         form = DepositForm(request.POST)
#         account = UserAccount.objects.filter(user = request.user).first()
#         if not account:
#             account = UserAccount.objects.create(balance = 0, user = request.user)
#         if form.is_valid():
#             tk = form.cleaned_data.get('deposit')
#             account.balance += tk
#             account.save()
#         messages.success(
#             request,
#             f'{"{:,.1f}".format(float(tk))}$ was deposited to your account successfully'
#         )
#         mail_subject = 'Deposit Confirmation'        
#         to_email = request.user.email
#         ConfarmationEmail(request.user ,to_email, "deposit", mail_subject, tk, 'confirmation_email.html')
#     else:
#         form = DepositForm()
#     return render(request, 'deposti.html', {'form': form})

@login_required
def Deposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        account = UserAccount.objects.filter(user=request.user).first()
        if not account:
            account = UserAccount.objects.create(balance=0, user=request.user)
        
        if form.is_valid():
            tk = form.cleaned_data.get('deposit')
            account.balance += tk
            account.save()
            messages.success(
                request,
                f'{"{:,.1f}".format(float(tk))}$ was deposited to your account successfully'
            )
            mail_subject = 'Deposit Confirmation'        
            to_email = request.user.email
            ConfarmationEmail(request.user, to_email, "deposit", mail_subject, tk, 'confirmation_email.html')
            return redirect('profile') 
    else:
        form = DepositForm()
    
    return render(request, 'deposti.html', {'form': form})


@login_required
def HotelLeave(request, id):
    user_data = request.user
    HotelBookingData.objects.get(pk = id).delete()
    return redirect('profile')


    
