from django.contrib import admin
from .models import Guest
# Register your models here.

@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'phone', 'email']
    search_fields = ['name', 'phone']
