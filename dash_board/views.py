from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main_page.models import Post
from .forms import post_form
from django.contrib.auth.decorators import login_required
from Advisor.models import Appointment
from Accounts.models import Profile
# Create your views here.
@login_required
def creat_post(request):
    profile = Profile.objects.get(user=request.user)
    user_posts = Post.objects.filter(author_id=request.user.id) 
    user_appointments = Appointment.objects.filter(client=request.user).order_by('-session_date')    
    
    if request.method == 'POST':
        form = post_form(request.POST,request.FILES)
        if form.is_valid:
            my_form = form.save(commit=False)
            my_form.author = request.user
            my_form.save()
           
            
            
    else :
        form = post_form()
        
    context = {'form':form,'user_posts':user_posts,
               'profile':profile,'user_appointments': user_appointments}
    return render(request,'dashboard_normal.html',context)


