from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main_page.models import Post
from .forms import post_form
# Create your views here.
@login_required
def creat_post(request):
    if request.method == 'POST':
        form = post_form(request.POST,request.FILES)
        if form.is_valid:
            my_form = form.save(commit=False)
            my_form.author = request.user
            my_form.save()
           
            
            
    else :
        form = post_form()
        
    context = {'form':form}
    return render(request,'dashboard_normal.html',context)