from django.contrib import admin
from django.contrib.auth import get_user_model

from jobbox.task.models import HRTask

UserModel = get_user_model()


@admin.register(HRTask)
class HRTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'status', 'user_id']
    ordering = ['id']
    list_filter = ['status']
    search_fields = ['task', 'user_id']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user_id':
            kwargs["queryset"] = UserModel.objects.filter(profilehr__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

