from django.contrib import admin

from .models import *

admin.site.register(Order)
admin.site.register(OrderInfo)
admin.site.register(BrowserHistory)
admin.site.register(ShoppingCart)
admin.site.register(ProductCollection)
admin.site.register(Sales)
admin.site.register(Comments)
