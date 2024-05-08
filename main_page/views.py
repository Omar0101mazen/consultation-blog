from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import render,redirect
from .models import Post
from django.core.paginator import Paginator
from .forms import post_form
from django.contrib.auth.decorators import login_required
from .filters import PostFilter
from django.db.models import Count
from .forms import CommentForm
from django.shortcuts import get_object_or_404, redirect
# Create your views here.


def post_list(request):
    post_list = Post.objects.all()
    myfilter = PostFilter(request.GET,queryset=post_list)
    post_list = myfilter.qs
    
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'posts':page_obj, 'myfilter' : myfilter}
    return render(request,'posts.html',context)



@login_required
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            # Check if the user is an advisor before saving
            if request.user.profile.account_type == 'advisor':
                comment.save()
                return redirect('mainpage:detail', slug=post.slug)
            else:
                # Handle cases where the user is not allowed to comment
                return HttpResponseForbidden("You are not authorized to comment.")
    else:
        comment_form = CommentForm()
    
    return render(request, 'post_detail.html', {'post': post, 'comment_form': comment_form})




def about(request):
    return render(request,'about.html')