from django.contrib import admin
from .models import Shop, Vendor, Product, Order
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
    list_display = ['nomi', 'rasmi']
    search_fields = ['nomi']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['vendor', 'shop', 'product', 'count', 'price', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['vendor', 'shop', 'product']