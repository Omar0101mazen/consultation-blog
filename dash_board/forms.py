from django import forms
from main_page.models import Post

class post_form(forms.ModelForm):
    class Meta:
      model = Post
      fields = ['title','content']
      
