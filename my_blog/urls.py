from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='my_blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    path('post/<slug:slug>/', views.post_detail_view, name='post_detail'),
    path('post/<slug:slug>/like/', views.like_toggle_view, name='like_toggle'),
    path('comment/<int:comment_id>/delete/', views.comment_delete_view, name='comment_delete'),
    
    path('dashboard/', views.author_dashboard_view, name='author_dashboard'),
    path('post/new/create/', views.post_create_view, name='post_create'),
    path('post/<slug:slug>/edit/', views.post_edit_view, name='post_edit'),
    path('post/<slug:slug>/delete/', views.post_delete_view, name='post_delete'),
    
    path('author/<str:username>/', views.author_profile_view, name='author_profile'),
]