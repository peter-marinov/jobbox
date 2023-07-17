from django.contrib import admin

from jobbox.app_auth.models import AppUser


# Register your models here.
@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    pass