from django.urls import path

from jobbox.note.views import CreateNote, EditUserNote, DeleteUserNote

urlpatterns = [
    path('create/', CreateNote.as_view(), name='create_note'),
    path('<int:pk>/edit/', EditUserNote.as_view(), name='edit_note'),
    path('<int:pk>/delete/', DeleteUserNote.as_view(), name='delete_note'),
]