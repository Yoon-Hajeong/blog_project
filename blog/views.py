from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Post, Comment
from .forms import PostForm, CommentForm
from accounts.models import Profile

User = get_user_model()

def base(request):
    return render(request, 'base.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/blog/')
        else:
            return render(request, 'accounts/login.html', {'error': '아이디 또는 비밀번호가 올바르지 않습니다.'})
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'accounts/logout.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {'error': '이미 존재하는 아이디입니다.'})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('/blog/')
    return render(request, 'accounts/register.html')

@login_required(login_url='/blog/login/')
def post_write(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()  
            return redirect('/blog/')
        else:
            print("폼 오류:", form.errors)
    else:
        form = PostForm()
    return render(request, 'blog/post_write.html', {'form': form})

def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('blog_list')

def post_search(request):
    tag = request.GET.get('q', '')
    if not tag:
        tag = request.resolver_match.kwargs.get('tag', '')
    
    posts = Post.objects.filter(
        Q(title__icontains=tag) | Q(category__icontains=tag)
    ).order_by('-id')
    
    return render(request, 'blog/post_search.html', {
        'tag': tag,
        'posts': posts
    })

def blog_list(request):
    posts = Post.objects.all().order_by('-id')
    return render(request, 'blog/blog_list.html', {'posts': posts})

# @login_required(login_url='/blog/login/')
def blog_detail(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return render(request, 'blog/post_not_found.html')
    
    post.views += 1
    post.save(update_fields=['views'])

    form = CommentForm()  # ✅ 댓글 폼 생성

    return render(request, 'blog/blog_detail.html', {
        'post': post,
        'form': form  # ✅ 템플릿에 전달!
    })

#댓글
@login_required(login_url='/blog/login/')
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    parent_id = request.POST.get('parent_id')
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        if parent_id:
            comment.parent = Comment.objects.get(id=parent_id)
        comment.save()
        
    return redirect('blog_detail', id=post.id)
    

@login_required(login_url='/blog/login/')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id
    if request.user == comment.author:
        comment.delete()
    return redirect('blog_detail', id=post_id)

@login_required(login_url='/blog/login/')
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.user != comment.author:
        return redirect('blog_detail', id=comment.post.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', id=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'blog/edit_comment.html', {
        'form': form,
        'comment': comment
    })
