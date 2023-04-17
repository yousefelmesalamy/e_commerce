from django.contrib import admin
from . models import *
# Register your models here.


class user (admin.ModelAdmin):
    list_display = ("pk", "username", "full_name", "email", "phone", "is_active", "usage_goal", "country")
    list_display_links = ("pk", "username")
    list_filter = ('username', "country")
    search_fields = ('username', 'phone',)


class product (admin.ModelAdmin):
    list_display = ("name", "price", "condition", "date_of_entry", "qty", "expired","stock")
    list_display_links = ('name',)
    list_filter = ("price", "name")
    search_fields = ('name', 'barcode',)


class cart_owner (admin.ModelAdmin):
    list_display = ("user",)
    list_display_links = ("user",)
    list_filter = ("user",)
    search_fields = ("user",)

class countrys (admin.ModelAdmin):
    list_display = ("country", "currency",)
    list_display_links = ("country",)
    list_filter = ("country",)
    search_fields = ("search_fields",)


class cart_detail(admin.ModelAdmin):
    list_display = ("products", "cart_owner", "coast_of_product")


class order (admin.ModelAdmin):
    list_display = ("cart", "num_of_products", "coast_of_products", "deliver_to")


admin.site.register(Order, order)
admin.site.register(Cart_detail, cart_detail)
admin.site.register(users, user)
admin.site.register(Products, product)
admin.site.register(Cart_Owner, cart_owner)
admin.site.register(Countrys, countrys)
