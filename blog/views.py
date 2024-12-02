from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import UserRegistrationForm, CommentForm, PostForm
from django.utils.text import slugify
from django.core.paginator import Paginator


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    comment_form = CommentForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            post_id = request.POST.get('post_id')
            post = Post.objects.get(id=post_id)
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_list')

    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'comment_form': comment_form})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = 'published'
            post.slug = slugify(post.title)
            post.save()
            return redirect('post_list')  # Редирект после успешного создания
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})

def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comment_form = CommentForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                return redirect('post_detail', post_id=post_id)

    return render(request, 'blog/post_detail.html', {'post': post, 'comment_form': comment_form})
