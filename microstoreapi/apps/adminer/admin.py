from django.contrib import admin

from .models import *


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('compony_name', 'addr', 'linkman')


admin.site.register(Supplier, SupplierAdmin)


class Supplier2ProductAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'product')


admin.site.register(Supplier2Product, Supplier2ProductAdmin)


class InventoryChangeAdmin(admin.ModelAdmin):
    list_display = ('product', 'supplier', 'change_type', 'count')


admin.site.register(InventoryChange, InventoryChangeAdmin)


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'inventory_num', 'current_invintory', 'sale_num')


admin.site.register(Inventory, InventoryAdmin)

