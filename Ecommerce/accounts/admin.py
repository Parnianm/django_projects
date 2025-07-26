from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


@admin.register(Account)
class AccountAdmin(UserAdmin):
    model = Account
    list_display = ('email', 'username', 'first_name', 'last_login', 'date_joined', 'last_name', 'is_active') 
    list_display_links = ('email', 'username', 'first_name')
    readonly_fields = ('last_login', 'date_joined')
    filter_horizontal = ()
    list_filter = ('is_staff', 'is_active', 'is_active')  
    ordering = ('date_joined',) 
    search_fields = ('email', 'username', 'first_name', 'last_name') 

