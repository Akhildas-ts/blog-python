from rest_framework import generics, permissions, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models
from .models import BlogPost
from .serializers import BlogPostSerializer, BlogPostCreateUpdateSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit their own posts.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the author
        return obj.author == request.user

class BlogPostListCreateView(generics.ListCreateAPIView):
    queryset = BlogPost.objects.filter(is_published=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'is_published']
    search_fields = ['title', 'content', 'tags']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BlogPostCreateUpdateSerializer
        return BlogPostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogPost.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BlogPostCreateUpdateSerializer
        return BlogPostSerializer

    def get_queryset(self):
        # Allow authors to see their unpublished posts
        if self.request.user.is_authenticated:
            return BlogPost.objects.filter(
                models.Q(is_published=True) | 
                models.Q(author=self.request.user)
            )
        return BlogPost.objects.filter(is_published=True)

class MyBlogPostsView(generics.ListAPIView):
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'tags']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']

    def get_queryset(self):
        return BlogPost.objects.filter(author=self.request.user)
