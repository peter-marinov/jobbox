from django.contrib import admin

from jobbox.common.models import Profile, ProfileHR


# Register your models here.
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(ProfileHR)
class ProfileAdmin(admin.ModelAdmin):
    pass
