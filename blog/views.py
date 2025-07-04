from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Post
from .forms import PostForm

def base(request):
    return render(request, 'base.html')

@login_required(login_url='/blog/login/')
def post_write(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()  # form.save() 대신 post.save() 사용
            return redirect('/blog/')
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
    """통합된 검색 기능 - URL 파라미터와 GET 파라미터 모두 처리"""
    tag = request.GET.get('q', '')
    if not tag:
        # URL에서 tag 파라미터 가져오기 (예: /search/diary/)
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

def blog_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/blog_detail.html', {'post': post})