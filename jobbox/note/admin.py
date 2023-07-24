from django.contrib import admin
from django.contrib.auth import get_user_model

from jobbox.note.models import UserNote

UserModel = get_user_model()


@admin.register(UserNote)
class UserNoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user_id']
    ordering = ['id']
    search_fields = ['title', 'user_id']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user_id':
            kwargs["queryset"] = UserModel.objects.filter(profile__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
