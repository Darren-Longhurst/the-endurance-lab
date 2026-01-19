from django.contrib import admin
from .models import Product, Category, ProductVariant

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'price',
        'rating',
        'image',
        'is_special_offer')

    ordering = ('sku', 'name')

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
        )

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'variant_type',
        'variant_value',
        'price_modifier',
        'stock_count',
    )
    ordering = ('product', 'variant_type', 'variant_value')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
