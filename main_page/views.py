from django.urls import reverse
from django.shortcuts import render,redirect
from .models import Post
from django.core.paginator import Paginator
from .forms import post_form
from django.contrib.auth.decorators import login_required
from .filters import PostFilter
from django.db.models import Count
# Create your views here.


def post_list(request):
    post_list = Post.objects.all()
    myfilter = PostFilter(request.GET,queryset=post_list)
    post_list = myfilter.qs
    
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'posts':page_obj, 'myfilter' : myfilter}
    return render(request,'posts.html',context)

# @login_required
# def post_detail(request,slug):
#     post_detail = Post.objects.get(slug=slug)
#     if request.method == 'POST':
#         form = post_form(request.POST,request.FILES)
#         if form.is_valid:
#             my_form = form.save(commit=False)
#             my_form.titl = post_detail
#             my_form.save()
           
            
            
#     else :
#         form = post_form()
        
#     context = {'post':post_detail,'form':form}
#     return render(request,'post_detail.html',context)

