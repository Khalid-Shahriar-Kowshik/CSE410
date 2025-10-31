from django.urls import path
from . import views

urlpatterns = [
    path('buildhub/', views.blog, name='blog'),
    path('AddBlog/', views.add_blog, name='addblog'),
    path('details/<int:blog_id>/', views.blog_details, name='blog_details'),
    path('like/<int:blog_id>/', views.like_blog, name='like_blog'),
    path('comment/<int:blog_id>/', views.add_comment, name='add_comment'),
    path('blog/<int:blog_id>/edit/', views.update_blog, name='update_blog'),
    path('blog/<int:blog_id>/delete/', views.delete_blog, name='delete_blog'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
     # Add the new URLs for search and autocomplete
    path('blog/search/', views.blog_search, name='blog_search'),
    path('blog/autocomplete/', views.blog_autocomplete, name='blog_autocomplete'),
]