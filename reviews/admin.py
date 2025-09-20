from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'product', 'user', 'rating', 
        'is_verified_purchase', 'created_at'
    ]
    list_filter = ['rating', 'is_verified_purchase', 'created_at', 'product__category']
    search_fields = ['title', 'content', 'product__name', 'user__username']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('product', 'user', 'title', 'content', 'rating')
        }),
        ('Additional Info', {
            'fields': ('is_verified_purchase', 'helpful_votes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ['product', 'user']
        return self.readonly_fields