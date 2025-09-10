from rest_framework import serializers
from .models import BlogPost
from accounts.serializers import UserSerializer

class BlogPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tag_list = serializers.ReadOnlyField()

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'is_published', 'tags', 'tag_list']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'is_published', 'tags']

    def validate_title(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long")
        return value.strip()

    def validate_content(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Content must be at least 10 characters long")
        return value.strip()
