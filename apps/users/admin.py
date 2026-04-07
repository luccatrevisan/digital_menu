from django.contrib import admin
from apps.users.models import CustomUser, Address


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'street', 'number']

admin.site.register(Address, AddressAdmin)

admin.site.register(CustomUser)