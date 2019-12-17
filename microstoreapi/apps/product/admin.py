from django.contrib import admin

from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'describe', 'price', 'category')
admin.site.register(Product)

admin.site.register(Category)
