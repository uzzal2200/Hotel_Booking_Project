
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from author.models import UserProfile


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'id' : 'required'}))
    image = forms.ImageField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ChangeProfileImage(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

class ChangeUserData(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email',]
        
class DepositForm(forms.Form):
    deposit = forms.DecimalField(max_digits=5, decimal_places=1)
