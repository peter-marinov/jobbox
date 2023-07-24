from django import forms
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from jobbox.task.models import HRTask


class UserProfileHRAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        user = self.request.current_user
        if hasattr(user, 'profilehr'):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponse('You do not have permission to access this page.', status=403)


class UserProfileHRAccessOwnTaskMixin:
    def dispatch(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.current_user
        if hasattr(user, 'profilehr') and user.pk == instance.user_id_id:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponse('You do not have permission to access this page.', status=403)


class CreateHRTask(auth_mixins.LoginRequiredMixin, UserProfileHRAccessMixin, views.CreateView):
    template_name = 'task/create_task.html'
    model = HRTask
    fields = ['task', 'status']
    success_url = reverse_lazy('profile_user')

    def form_valid(self, form):
        user_note_form = form.save(commit=False)
        user_note_form.user_id = self.request.user
        user_note_form.save()
        return super().form_valid(form)


class ListHRTask(auth_mixins.LoginRequiredMixin, UserProfileHRAccessMixin, views.ListView):
    template_name = 'task/user_hr_tasks.html'
    model = HRTask

    def get_queryset(self):
        tasks = HRTask.objects.filter(user_id=self.request.current_user.pk)
        return tasks


class EditHRTask(auth_mixins.LoginRequiredMixin, UserProfileHRAccessOwnTaskMixin, views.UpdateView):
    template_name = 'task/edit_task.html'
    model = HRTask
    fields = ['task', 'status']
    success_url = reverse_lazy('list_hr_task')


class DeleteHRTask(auth_mixins.LoginRequiredMixin, UserProfileHRAccessOwnTaskMixin, views.DeleteView):
    template_name = 'task/delete_task.html'
    model = HRTask
    success_url = reverse_lazy('list_hr_task')