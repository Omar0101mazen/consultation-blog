from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login, logout

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data.get('password1')
            user.set_password(raw_password)
            user.save()

            # التحقق من وجود ملف التعريف قبل الحفظ
            if 'photo' in request.FILES:
                form.save()

            # تحقق من وجود ملف التعريف قبل الحفظ
            if hasattr(user, 'profile'):
                profile = user.profile
                profile.account_type = form.cleaned_data.get('account_type')
                profile.experiences = form.cleaned_data.get('experiences')
                profile.certificates = form.cleaned_data.get('certificates')
                profile.save()

            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect_to_user_dashboard(user)  # توجيه المستخدم إلى لوحة التحكم
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def custom_login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect_to_user_dashboard(user)  # توجيه المستخدم إلى لوحة التحكم
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def redirect_to_user_dashboard(user):
    if user.profile.account_type == 'advisor':
        return redirect('dashboard_m:create_moral')  # URL لوحة تحكم المستشارين
    else:
        return redirect('dashboard_n:create_normal')  # URL لوحة تحكم المستخدمين العاديين

def custom_logout_view(request):
    logout(request)
    return redirect('/')  # توجيه المستخدم إلى الصفحة الرئيسية بعد تسجيل الخروج
