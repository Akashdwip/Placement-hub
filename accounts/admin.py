
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('PlacementHub Role', {'fields': ('role',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('PlacementHub Role', {'fields': ('role',)}),
    )

    list_display = (
        'username',
        'email',
        'role',
        'is_staff',
        'is_active',
    )
