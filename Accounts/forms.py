
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
    
    photo = forms.ImageField(
        label='الصورة',
        required=False ,
        
        
    )
    account_type = forms.ChoiceField(
        choices=Profile.ACCOUNT_TYPES, 
        required=True, 
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=''
    )
    certificates = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('الشهادات الحاصل عليها')}),
        label=''  
    )
    experiences = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': _('الخبرات')}),
        label=''  
    )
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['account_type'].initial = 'normal'

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'photo', 'account_type','certificates','experiences')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # تأكد من حصولك على ملف التعريف بعد إنشاء المستخدم
            profile, created = Profile.objects.get_or_create(user=user)
            profile.account_type = self.cleaned_data['account_type']
            profile.photo = self.cleaned_data['photo'] 
            profile.certificates = self.cleaned_data['certificates']
            profile.experiences = self.cleaned_data['experiences']
            
            profile.save()
        return user
        

        
        

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

