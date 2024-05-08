
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User
from .models import Profile
from django.utils.translation import gettext_lazy as _
from .models import Profile


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('اسم المستخدم')}),
        label=''  
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('كلمة المرور')}),
        label=''  
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': _('تأكيد كلمة المرور')}),
        label=''  
    )
    email = forms.EmailField(
        max_length=254, 
    
        widget=forms.EmailInput(attrs={'placeholder': _('البريد الإلكتروني')}),
        label=''
    )
    
 


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


        

        
        

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(attrs={'placeholder': 'اسم المستخدم'}),
        label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'كلمة المرور'}),
        label=''
    )



# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['photo','appointment1','appointment2','appointment3','appointment4','appointment5'] 