from django.contrib import admin
from django.contrib.admin import site
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


class CustomUserAdmin(admin.ModelAdmin):
    list_filter = UserAdmin.list_filter + ("email", "username")
    list_display = UserAdmin.list_display


site.unregister(User)
site.register(User, CustomUserAdmin)
