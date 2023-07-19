from django.contrib import admin

from jobbox.app_auth.models import AppUser


# Register your models here.
@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'is_superuser', 'is_staff']
    ordering = ['id']
    list_filter = ['is_superuser', 'is_staff']