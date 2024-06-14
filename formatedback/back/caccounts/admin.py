from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('phone', 'email', 'name', 'is_staff', 'id')
    search_fields = ('phone', 'name', 'email')
    ordering = ('phone',)

    filter_horizontal = ()
    list_filter = ()

    fieldsets = (
        (None, {'fields': ('phone', 'email', 'name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)