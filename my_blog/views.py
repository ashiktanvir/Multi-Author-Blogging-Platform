from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.http import HttpResponseForbidden
from .models import Post, Category, Tag, Comment, Like
from .forms import UserRegisterForm, PostForm, CommentForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'my_blog/register.html', {'form': form})

def home_view(request):
    posts_list = Post.objects.filter(status='Published').select_related('author', 'category').prefetch_related('tags')
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        posts_list = posts_list.filter(Q(title__icontains=query) | Q(content__icontains=query))

    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        posts_list = posts_list.filter(category__name__iexact=category_slug)

    # Tag filter
    tag_slug = request.GET.get('tag')
    if tag_slug:
        posts_list = posts_list.filter(tags__name__iexact=tag_slug)

    paginator = Paginator(posts_list, 5) # 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'my_blog/home.html', context)

def post_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Prevent non-authors/non-admins from viewing draft posts
    if post.status == 'Draft':
        if not request.user.is_authenticated or (request.user != post.author and not request.user.is_superuser):
            return HttpResponseForbidden("You do not have permission to view this draft.")

    # Increment View Count safely in session to avoid unnecessary duplicate increments on refresh
    session_key = f"viewed_post_{post.pk}"
    if not request.session.get(session_key, False):
        Post.objects.filter(pk=post.pk).update(view_count=F('view_count') + 1)
        request.session[session_key] = True
        post.refresh_from_db()

    comments = post.comments.all()
    comment_form = CommentForm()

    # Check if logged-in user liked this post
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = Like.objects.filter(post=post, user=request.user).exists()

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect('post_detail', slug=post.slug)

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_has_liked': user_has_liked,
    }
    return render(request, 'my_blog/post_detail.html', context)

@login_required
def like_toggle_view(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete() # Toggle off
    return redirect('post_detail', slug=post.slug)

@login_required
def comment_delete_view(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    # Moderation check: Commenter, Post Author, or Superuser can delete
    if request.user == comment.user or request.user == comment.post.author or request.user.is_superuser:
        post_slug = comment.post.slug
        comment.delete()
        return redirect('post_detail', slug=post_slug)
    return HttpResponseForbidden("You are not authorized to delete this comment.")

# --- Author Dashboard Views ---

@login_required
def author_dashboard_view(request):
    if not request.user.profile.is_author and not request.user.is_superuser:
        return HttpResponseForbidden("Access restricted to approved Authors only.")
    
    author_posts = Post.objects.filter(author=request.user)
    return render(request, 'my_blog/author_dashboard.html', {'posts': author_posts})

@login_required
def post_create_view(request):
    if not request.user.profile.is_author and not request.user.is_superuser:
        return HttpResponseForbidden("Only approved Authors can create posts.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('author_dashboard')
    else:
        form = PostForm()
    return render(request, 'my_blog/post_form.html', {'form': form, 'title': 'Create New Post'})

@login_required
def post_edit_view(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # View-level permission check: Only post author or superuser can edit
    if request.user != post.author and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to edit someone else's post.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('author_dashboard')
    else:
        form = PostForm(instance=post)
    return render(request, 'my_blog/post_form.html', {'form': form, 'title': 'Edit Post', 'post': post})

@login_required
def post_delete_view(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # View-level permission check: Only post author or superuser can delete
    if request.user != post.author and not request.user.is_superuser:
        return HttpResponseForbidden("You are not allowed to delete someone else's post.")

    if request.method == 'POST':
        post.delete()
        return redirect('author_dashboard')
    return render(request, 'my_blog/post_confirm_delete.html', {'post': post})

def author_profile_view(request, username):
    author = get_object_or_404(User, username=username)
    published_posts = Post.objects.filter(author=author, status='Published')
    return render(request, 'my_blog/author_profile.html', {'author': author, 'posts': published_posts})