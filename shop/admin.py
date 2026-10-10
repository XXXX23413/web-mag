from django.contrib import admin
from .models import (Category,Brand, Product,ProductSpecification,Cart,CartItem, Order, OrderItem,Review)

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra  = 1

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra=1

class OrderItemInline(admin.TabularInline):
    model=OrderItem
    extra=1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','slug','is_active','created_at')
    list_filter=('is_active',)
    prepopulated_fields={'slug':('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name','slug','is_active')
    list_filter=('is_active',)
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','category','brand','price','stock_quantity','is_active','created_at')
    list_filter=('category','brand','is_active')
    search_fields=('name','description')
    prepopulated_fields={'slug':('name',)}
    inlines = [ProductSpecificationInline]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id','user','created_at')
    inlines = [CartItemInline]



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=('number','customer_name','phone','created_at','status','total_amount')
    list_filter=('status','payment_status','created_at')
    search_fields=('number','customer_name','phone','email')
    inlines=[OrderItemInline]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product','user','rating','is_published','created_at')
    list_filter = ('rating','is_published')
    actions = ['publish_reviews']

    @admin.action(description="Опубликовать выбранные отзывы")
    def publish_reviews(self,request,queryset):
        queryset.update(is_published=True)

admin.site.register(ProductSpecification)
admin.site.register(CartItem)    
admin.site.register(OrderItem) 

