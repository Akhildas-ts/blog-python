from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated tags")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def tag_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
        return []
