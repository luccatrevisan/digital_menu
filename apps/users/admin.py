from django.contrib import admin
from apps.users.models import CustomUser, Address


class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'street', 'number']

admin.site.register(Address, AddressAdmin)

admin.site.register(CustomUser) # TO-DO: for user management, it can be useful to customize the user admin page