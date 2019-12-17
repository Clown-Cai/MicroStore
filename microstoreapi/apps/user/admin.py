from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy

from .models import *


class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'password', 'is_superuser', 'is_staff', 'is_active', 'avatar', 'email', 'phone')
    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email')}),

        (gettext_lazy('User Information'), {'fields': ('phone', 'avatar')}), # 自己加的字段

        (gettext_lazy('Permissions'), {'fields': ('is_superuser', 'is_staff', 'is_active',
                                                  'groups', 'user_permissions')}),

        (gettext_lazy('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

# admin.site.register(User, UserAdmin)
admin.site.register(User, UserProfileAdmin)


class IntegralAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_integral', 'increase_integral')


admin.site.register(Integral, IntegralAdmin)

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'addr', 'consignee')

admin.site.register(Address, AddressAdmin)


class UserIntegralAdmin(admin.ModelAdmin):
    list_display = ('user', 'integral_num', 'current_integral', 'cost_num')

admin.site.register(UserIntegral, UserIntegralAdmin)
