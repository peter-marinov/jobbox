from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import resolve

from jobbox.common.models import ProfileHR, ContactUs

UserModel = get_user_model()


@admin.register(ProfileHR)
class ProfileHRAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'first_name', 'last_name', 'company_name', 'telephone_number']
    ordering = ['-user_id']
    list_filter = ['company_name']
    search_fields = ['first_name', 'last_name', 'company_name', 'telephone_number']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            # Get the view's arguments and resolve the object_id from the URL
            resolved_url = resolve(request.path_info)
            object_id = resolved_url.kwargs.get('object_id')
            if object_id:
                kwargs["queryset"] = UserModel.objects.filter(pk=object_id)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'topic']
    ordering = ['-id']
    search_fields = ['email', 'topic']
