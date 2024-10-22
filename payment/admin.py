from django.contrib import admin

from .models import Order, OrderItem, ShippingAddress

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'shipping_address', 'amount', 'created', 'updated')
    ordering = ('-created',)

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'order', 'product', 'price', 'quantity')
    ordering = ('order',)

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'country', 'city', 'street_address', 'email')
    ordering = ('full_name',)

