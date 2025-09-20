import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q, Avg
from .models import Product, Category

class ProductFilter(filters.FilterSet):
    # Price range filters
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    price_range = filters.RangeFilter(field_name="price")
    
    # Category filters (including parent categories)
    category = filters.ModelChoiceFilter(queryset=Category.objects.filter(is_active=True))
    category_name = filters.CharFilter(field_name="category__name", lookup_expr='icontains')
    
    # Stock filters
    stock_status = filters.ChoiceFilter(choices=Product.STOCK_STATUS_CHOICES)
    in_stock = filters.BooleanFilter(method='filter_in_stock')
    low_stock_threshold = filters.NumberFilter(method='filter_low_stock')
    
    # Rating filters
    min_rating = filters.NumberFilter(method='filter_min_rating')
    rating_gte = filters.NumberFilter(method='filter_rating_gte')
    
    # Active/availability filters
    is_active = filters.BooleanFilter()
    is_available = filters.BooleanFilter(method='filter_is_available')
    
    # Date filters
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')
    
    # Seller filter
    seller = filters.CharFilter(field_name="created_by__username", lookup_expr='icontains')
    
    # Advanced search
    search = filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'icontains'],
            'sku': ['exact', 'icontains'],
            'stock_quantity': ['exact', 'gte', 'lte'],
        }

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock_quantity__gt=0, is_active=True)
        return queryset

    def filter_is_available(self, queryset, name, value):
        if value:
            return queryset.filter(stock_quantity__gt=0, is_active=True)
        elif value is False:
            return queryset.filter(Q(stock_quantity=0) | Q(is_active=False))
        return queryset

    def filter_low_stock(self, queryset, name, value):
        """Filter products with stock below threshold"""
        return queryset.filter(stock_quantity__lte=value, stock_quantity__gt=0)

    def filter_min_rating(self, queryset, name, value):
        """Filter products with minimum average rating"""
        return queryset.annotate(
            avg_rating=Avg('reviews__rating')
        ).filter(avg_rating__gte=value)

    def filter_rating_gte(self, queryset, name, value):
        """Filter products with rating greater than or equal to value"""
        return queryset.annotate(
            avg_rating=Avg('reviews__rating')
        ).filter(avg_rating__gte=value)

    def filter_search(self, queryset, name, value):
        """Advanced search across multiple fields"""
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value) |
            Q(category__name__icontains=value) |
            Q(sku__icontains=value)
        ).distinct()

class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    has_products = filters.BooleanFilter(method='filter_has_products')
    parent = filters.ModelChoiceFilter(queryset=Category.objects.filter(is_active=True))
    is_parent = filters.BooleanFilter(method='filter_is_parent')
    
    class Meta:
        model = Category
        fields = ['is_active', 'parent']

    def filter_has_products(self, queryset, name, value):
        if value:
            return queryset.filter(products__isnull=False).distinct()
        return queryset.filter(products__isnull=True)

    def filter_is_parent(self, queryset, name, value):
        if value:
            return queryset.filter(children__isnull=False).distinct()
        return queryset.filter(children__isnull=True)