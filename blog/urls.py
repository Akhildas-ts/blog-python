from django.urls import path
from . import view

urlpatterns = [
    path('posts/', view.BlogPostListCreateView.as_view(), name='blogpost-list-create'),
    path('posts/<int:pk>/', view.BlogPostDetailView.as_view(), name='blogpost-detail'),
    path('my-posts/', view.MyBlogPostsView.as_view(), name='my-blogposts'),
]
