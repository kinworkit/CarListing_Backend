from django.contrib import admin
from .models import Cars, Complect


@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    list_display = ('mark', 'model', 'price', 'city', 'user')
    search_fields = ('mark', 'model', 'price', 'city')
    ordering = ('user',)


@admin.register(Complect)
class ComplectAdmin(admin.ModelAdmin):

    list_display = ("field_as_boolean",)

    def field_as_boolean(self, obj):
        return True if obj.field else False

    field_as_boolean.boolean = True
    field_as_boolean.short_description = "field_name"
