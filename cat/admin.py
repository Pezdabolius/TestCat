from django.contrib import admin
from .models import Kitten


@admin.register(Kitten)
class KittenAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'breed', 'color', 'age', 'owner']
    list_display = ['name', 'breed', 'color', 'age', 'owner']
    search_fields = ['breed']
