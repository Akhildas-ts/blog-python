from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField(blank=True)
    is_verified_purchase = models.BooleanField(default=False)
    helpful_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['product', 'user']  # One review per user per product
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rating}★ review for {self.product.name} by {self.user.username}"

    def save(self, *args, **kwargs):
        # Check if user has purchased this product
        from orders.models import OrderItem, Order
        user_orders = Order.objects.filter(
            user=self.user, 
            status__in=['delivered', 'confirmed'],
            items__product=self.product
        )
        if user_orders.exists():
            self.is_verified_purchase = True
        
        super().save(*args, **kwargs)

class ReviewHelpful(models.Model):
    """Track which users found reviews helpful"""
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='helpful_votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['review', 'user']

    def __str__(self):
        return f"{self.user.username} found review helpful"