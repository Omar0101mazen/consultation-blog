from django.shortcuts import render
from .forms import SignUpForm ,LoginForm
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from .forms import LoginForm
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)  # إضافة request.FILES لدعم تحميل الملفات
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # تحميل البيانات الجديدة من قاعدة البيانات
            # تحديث بيانات profile بناءً على البيانات المُدخلة في النموذج
            profile = user.profile
            profile.phone_number1 = form.cleaned_data.get('phone_number1','')
            profile.phone_number2 = form.cleaned_data.get('phone_number2', '')

            profile.save()
            
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            
            # توجيه المستخدم بناءً على نوع الحساب
            if user.profile.account_type == 'advisor':
                return redirect('dashboard_m:create_moral')  # توجيه المستخدمين من نوع "شركة" إلى لوحة تحكم الشركات
            else:
                return redirect('dashboard_n:create_normal')  # توجيه المستخدمين من نوع "شخصي" إلى صفحة الرئيسية
            
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})




def redirect_to_user_dashboard(user):
    if user.profile.account_type == 'advisor':
        return redirect('dashboard_m:create_moral')  # لوحة تحكم الشركات
    else:
        return redirect('dashboard_n:create_normal') 
    
@receiver(user_logged_in)
def direct_to_dashboard(sender, request, user, **kwargs):
    # تحديد نوع الحساب وتوجيه المستخدم بناءً عليه
    if user.profile.account_type == 'advisor':
        redirect_url = 'dashboard_m:create_moral'  # URL لوحة تحكم الشركات
    else:
        redirect_url = 'dashboard_n:create_normal'  # URL الصفحة الرئيسية للمستخدمين الأفراد
    # يجب استخدام redirect هنا بدلاً من return
    request.session['redirect_url'] = redirect_url





def custom_logout_view(request):
    logout(request)
    return redirect('/') 


# في ملف views.py

def custom_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # التحقق من نوع الحساب والتوجيه
                # if user.profile.account_type == 'advisor':
                #     return redirect('dashboard_m:create_moral')
                # else:
                #     return redirect('dashboard_n:create_normal')
    else:
        form = LoginForm()  # إنشاء نموذج فارغ لحالة GET
    return render(request, 'registration/login.html', {'form': form})
