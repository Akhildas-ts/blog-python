from rest_framework import permissions
from orders.models import Order, OrderItem

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only for the owner
        return obj.created_by == request.user

class IsSellerOrReadOnly(permissions.BasePermission):
    """
    Permission for product sellers - only creators can edit their products
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return hasattr(obj, 'created_by') and obj.created_by == request.user

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission for admin-only write operations (like categories)
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsOrderOwner(permissions.BasePermission):
    """
    Permission to only allow order owners to view/edit their orders
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class CanReviewProduct(permissions.BasePermission):
    """
    Permission to only allow users who bought the product to review it
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # For review creation, check if user has purchased the product
        if hasattr(view, 'get_product'):
            product = view.get_product()
            # Check if user has ordered this product
            user_orders = Order.objects.filter(
                user=request.user,
                status__in=['delivered', 'confirmed'],
                items__product=product
            )
            return user_orders.exists()
        
        # For review editing, only allow the review author
        return obj.user == request.user

class IsReviewOwner(permissions.BasePermission):
    """
    Permission to only allow review owners to edit their reviews
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user