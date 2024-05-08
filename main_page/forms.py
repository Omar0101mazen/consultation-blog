from django import forms
from .models import Post,Comment

class post_form(forms.ModelForm):
    class Meta:
      model = Post
      fields = ['title','content']
      
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']