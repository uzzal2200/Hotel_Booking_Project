from .models import Comment, RatingModel
from django import forms
from .models import Post
      
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body', ]

class RatingForm(forms.ModelForm):
    class Meta:
        model = RatingModel
        fields = ['rating']
        