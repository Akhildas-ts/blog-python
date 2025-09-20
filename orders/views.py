from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, OrderItem
from .serializers import (
    OrderListSerializer,
    OrderDetailSerializer,
    OrderItemSerializer,
    CreateOrderSerializer
)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()  # ADD THIS LINE
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'payment_status']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all().select_related('user').prefetch_related('items__product')
        return Order.objects.filter(user=self.request.user).select_related('user').prefetch_related('items__product')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateOrderSerializer
        elif self.action == 'list':
            return OrderListSerializer
        return OrderDetailSerializer

class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OrderItem.objects.all()  # ADD THIS LINE
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return OrderItem.objects.all().select_related('order', 'product')
        return OrderItem.objects.filter(order__user=self.request.user).select_related('order', 'product')