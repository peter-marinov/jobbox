from django.contrib import admin
from django.contrib.auth import get_user_model

from jobbox.job.models import Job
UserModel = get_user_model()


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'programming_language', 'salary', 'hr']
    ordering = ['id']
    list_filter = ['title', 'programming_language', 'salary']
    search_fields = ['title', 'programming_language', 'salary', 'hr']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'hr':
            kwargs["queryset"] = UserModel.objects.filter(profilehr__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

