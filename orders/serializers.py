from rest_framework import serializers
from .models import Order, OrderItem
from decimal import Decimal


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_name', 'product_image',
            'quantity', 'unit_price', 'total_price'
        ]
        read_only_fields = ['total_price']
    
    def get_total_price(self, obj):
        return obj.get_total()


class OrderListSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'user_name', 'status', 
            'payment_status', 'total_amount', 'items_count', 'created_at'
        ]
        read_only_fields = ['order_number', 'created_at']
    
    def get_items_count(self, obj):
        return obj.items.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'user_name', 'status', 'payment_status',
            'subtotal', 'tax_amount', 'shipping_amount', 'total_amount',
            'shipping_name', 'shipping_address_line1', 'shipping_address_line2',
            'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country',
            'notes', 'tracking_number', 'items',
            'created_at', 'updated_at', 'shipped_at', 'delivered_at'
        ]
        read_only_fields = ['order_number', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.ModelSerializer):
    items = serializers.ListField(child=serializers.DictField(), write_only=True)
    
    class Meta:
        model = Order
        fields = [
            'shipping_name', 'shipping_address_line1', 'shipping_address_line2',
            'shipping_city', 'shipping_state', 'shipping_postal_code', 
            'shipping_country', 'notes', 'items'
        ]
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # Create the order
        order = Order.objects.create(user=user, **validated_data)
        
        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                unit_price=item_data.get('unit_price', None)
            )
        
        # Calculate totals
        order.calculate_total()
        
        return order
