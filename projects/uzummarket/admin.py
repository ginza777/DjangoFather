from django.contrib import admin
from .models import Shop, Vendor, Product, Order
from django.utils.html import format_html
# Register your models here.

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'manzili', 'telefon', 'extra', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['nomi', 'manzili', 'telefon']

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['nomi', 'image_html']
    search_fields = ['nomi']

    def image_html(self, obj):
        if obj.rasmi:
            return format_html(f'<img src="{obj.rasmi.url}" width="100" height="100" />')
        return None

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'shop', 'product', 'count', 'price', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['vendor', 'shop', 'product']