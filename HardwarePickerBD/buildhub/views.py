from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BlogForm, CommentForm
from .models import BlogPost, Like, Comment
from django.db.models import Count
from django.http import JsonResponse
from django.urls import reverse
from django.db.models import Q


def blog(request):
    blogs = BlogPost.objects.annotate(like_count=Count('likes'))
    sort_by = request.GET.get('sort', 'date')
    if sort_by == 'likes':
        blogs = blogs.order_by('-like_count', '-created')
    else:
        blogs = blogs.order_by('-created')

    return render(request, 'buildhub/blog.html', {'blog': blogs})


@login_required
def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('blog')
    else:
        form = BlogForm()
    return render(request, 'buildhub/blog_form.html', {'form': form, 'update': False})


def blog_details(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    return render(request, 'buildhub/blog_details.html', {'blog': blog})


@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    like, created = Like.objects.get_or_create(blog=blog, user=request.user)
    if not created:
        like.delete()  # Unlike if already liked
    return redirect('blog_details', blog_id=blog.id)


@login_required
def add_comment(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
            return redirect('blog_details', blog_id=blog.id)
    else:
        form = CommentForm()
    return render(request, 'buildhub/comment_form.html', {'form': form, 'blog': blog})


@login_required
def update_blog(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id, author=request.user)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog_details', blog_id=blog.id)
    else:
        form = BlogForm(instance=blog)
    return render(request, 'buildhub/blog_form.html', {'form': form, 'update': True})


@login_required
def delete_blog(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id, author=request.user)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog')
    return render(request, 'buildhub/delete_blog_form.html', {'blog': blog})


@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog_details', blog_id=comment.blog.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'buildhub/comment_form.html', {'form': form, 'comment': comment, 'blog': comment.blog})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        blog_id = comment.blog.id
        comment.delete()
        return redirect('blog_details', blog_id=blog_id)
    return render(request, 'buildhub/delete_comment_form.html', {'comment': comment})


# --- Search and Autocomplete Views (FIXED) ---

def blog_search(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        results = BlogPost.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).distinct()
        
    return render(request, 'buildhub/blog_search_results.html', {  # FIXED PATH
        'query': query,
        'results': results,
    })


def blog_autocomplete(request):
    # Accommodate both 'term' (from jQuery UI) and 'q' (from your JS)
    term = request.GET.get('term', '') or request.GET.get('q', '')
    term = term.strip()
    
    suggestions = []
    if term:
        posts = BlogPost.objects.filter(title__icontains=term)[:8]
        for post in posts:
            thumbnail_url = post.display_image.url if post.display_image else ''
            detail_url = reverse('blog_details', args=[post.id])

            suggestions.append({
                'label': post.title,
                'value': post.title,
                'url': detail_url,
                'thumbnail': thumbnail_url,
                'author': post.author.username
            })
            
    return JsonResponse(suggestions, safe=False)
