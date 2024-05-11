from django.http import HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import render,redirect
from .models import Post,Comment,CommentRating
from django.core.paginator import Paginator
from .forms import post_form
from django.contrib.auth.decorators import login_required
from .filters import PostFilter
from django.db.models import Count
from .forms import CommentForm
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Avg

# Create your views here.


from django.db.models import Count
def highest_rated_comment():
    highest_rated_comment = Comment.objects.annotate(avg_rating=Avg('ratings__rating')).order_by('-avg_rating')[:3]
    return highest_rated_comment
def post_list(request):
    top_comments = highest_rated_comment()
    post_list = Post.objects.annotate(comment_count=Count('comments'))
    myfilter = PostFilter(request.GET, queryset=post_list)
    post_list = myfilter.qs
    
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {'posts': page_obj, 'top_comments': top_comments, 'myfilter': myfilter}
    return render(request, 'posts.html', context)




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


def rate_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST' and request.user.profile.account_type == 'advisor':
        rating = request.POST.get('rating')
        CommentRating.objects.update_or_create(
            user=request.user,
            comment=comment,
            defaults={'rating': rating}
        )
        return redirect('mainpage:detail', slug=comment.post.slug)
    else:
        return HttpResponseForbidden("You are not authorized to rate comments.")
    




