from django.contrib import admin
from .models import Category, Product, Order, OrderItem

class OrderItemInLine(admin.TabularInline):
    model=OrderItem
    extra=1
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','slug')
    prepopulated_fields={'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','category','price','is_available','created_at')
    list_filter=('category','is_available')
    prepopulated_fields={'slug':('name',)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('id','customer_name','phone','created_at','status')
    list_filter=('status',)
    inlines=[OrderItemInLine]
admin.site.register(OrderItem) 

