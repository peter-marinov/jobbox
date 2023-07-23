from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from jobbox.note.models import UserNote


class UserProfileAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        user = self.request.current_user
        if hasattr(user, 'profile'):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponse('You do not have permission to access this page.', status=403)


class CreateNote(auth_mixins.LoginRequiredMixin, UserProfileAccessMixin, views.CreateView):
    template_name = 'note/create_note.html'
    model = UserNote
    fields = ['title', 'description']
    success_url = reverse_lazy('profile_user')

    def form_valid(self, form):
        user_note_form = form.save(commit=False)
        user_note_form.user_id = self.request.user
        user_note_form.save()
        return super().form_valid(form)


class EditUserNote(auth_mixins.LoginRequiredMixin, UserProfileAccessMixin, views.UpdateView):
    template_name = 'note/edit_note.html'
    model = UserNote
    fields = ['title', 'description']
    success_url = reverse_lazy('profile_user')


class DeleteUserNote(auth_mixins.LoginRequiredMixin, UserProfileAccessMixin, views.DeleteView):
    template_name = 'note/delete_note.html'
    model = UserNote
    success_url = reverse_lazy('profile_user')



