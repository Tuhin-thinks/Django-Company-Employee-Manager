from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Company, User


class CustomUserAdmin(UserAdmin):
    list_display = ("email", "first_name", "last_name", "company_name", "is_user", "is_admin")
    list_filter = ("is_user", "is_admin")
    fieldsets = (
        (None, {"fields": ("email", "company")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_user", "is_admin")}),
    )
    add_fieldsets = (
        (None, {"fields": ("email", "password1", "password2", "company")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_user", "is_admin")}),
    )
    search_fields = ("email", "company__name")

    def company_name(self, obj):
        if obj.company:
            return obj.company.name
        else:
            return "NA"

    company_name.short_description = "Company"  # Sets the column header in the admin list
    company_name.admin_order_field = "company__name"  # Allows ordering by company name
    ordering = ("email", "company__name")


# Register your models here.
admin.site.register(Company)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
