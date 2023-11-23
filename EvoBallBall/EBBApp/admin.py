from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Product, Buyer, Comment, Order

# Register your models here.
admin.site.site_header = 'EvoBallBall Admin'
admin.site.index_title = 'EvoBallBall Administration'
admin.site.site_title = 'EvoBallBall Administration'


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'delivery_information']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_show', 'slug', 'price', 'on_sale', 'available']
    list_filter = ['available']
    list_editable = ['price', 'on_sale', 'available']
    prepopulated_fields = {'slug': ('name',)}

    def image_show(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' width='60' />")
        return "None"

    image_show.__name__ = "Image"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'comment', 'created_by']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'email',  'delivery_information', 'product', 'quantity', 'status']
    list_editable = ['status']
    list_filter = ['user', 'status']

    def delivery_information(self, obj):
        return obj.user.delivery_information

    def email(self, obj):
        return obj.user.email

    delivery_information.__name__ = "Delivery information"
