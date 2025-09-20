from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().select_related('user', 'product')
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rating', 'product', 'is_verified_purchase']
    ordering = ['-created_at']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        """Custom delete method that returns review details"""
        try:
            instance = self.get_object()
            # Get the review data before deletion
            review_data = ReviewSerializer(instance).data
            review_title = instance.title or f"{instance.rating}★ review"
            product_name = instance.product.name
            user_name = instance.user.username
            
            # Delete the review
            self.perform_destroy(instance)
            
            return Response({
                'message': f'Review "{review_title}" for product "{product_name}" by {user_name} successfully deleted',
                'deleted_review': review_data,
                'status': 'success'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': f'Failed to delete review: {str(e)}',
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
