from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from .forms import SignUpForm,LoginForm
from .models import Profile

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            raw_password = form.cleaned_data.get('password1')
            user.set_password(raw_password)
            user.save()
            
            # Create or update user profile with additional data from the HTML form
            profile, created = Profile.objects.get_or_create(user=user)
            profile.account_type = request.POST.get('account_type', 'normal')
            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']
            profile.experiences = request.POST.get('experiences', '')
            profile.certificates = request.POST.get('certificates', '')
            profile.save()

            user = authenticate(username=user.username, password=raw_password)
            if user.profile.account_type == 'advisor':
                    return redirect('advisor:advisor_dashboard')  # توجيه المستخدمين من نوع "شركة" إلى لوحة تحكم الشركات
            else:
                    return redirect('dashboard:creat_post') 
            
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
        return redirect('advisor:advisor_dashboard')  # URL لوحة تحكم المستشارين
    else:
        return redirect('dashboard:creat_post')  # URL لوحة تحكم المستخدمين العاديين

def custom_logout_view(request):
    logout(request)
    return redirect('/')  # توجيه المستخدم إلى الصفحة الرئيسية بعد تسجيل الخروج


