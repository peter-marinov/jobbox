import os

from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.contrib.auth import mixins as auth_mixins

from jobbox.app_auth.forms import RegisterUserForm, RegisterUserHRForm, EditUserHRForm, EditUserForm
from jobbox.app_auth.models import AppUser
from jobbox.job.models import Job
from jobbox.note.models import UserNote

UserModel = get_user_model()


class LoginUserView(auth_views.LoginView):
    template_name = 'app_auth/login.html'


class RegisterUserView(views.CreateView):
    template_name = 'app_auth/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'USER'

        return context


class RegisterHRView(views.CreateView):
    template_name = 'app_auth/register-hr.html'
    form_class = RegisterUserHRForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'HR'

        return context

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)

        return result


class LogoutUserView(auth_views.LogoutView):
    pass


def check_if_account_is_user_or_hr(request):
    if hasattr(request.current_user, 'profilehr'):
        user_type = 'hr'
        return request.current_user.profilehr, user_type
    else:
        user_type = 'user'
        return request.current_user.profile, user_type


@login_required
def profile_user(request):
    user, user_type = check_if_account_is_user_or_hr(request)
    notes = UserNote.objects.filter(user_id=user.pk)
    context = {
        'user': user,
        'user_type': user_type,
        'notes': notes,
    }
    return render(request, 'app_auth/profile.html', context=context)


@login_required
def update_profile(request):
    user, user_type = check_if_account_is_user_or_hr(request)

    if user_type == AppUser.PROFILE_USER:
        initial_data = {
            'first_name': user.first_name,
        }
        edit_form = EditUserForm
    else:
        initial_data = {
            'first_name': user.first_name,
            'company_name': user.company_name,
        }
        edit_form = EditUserHRForm

    if request.method == 'GET':
        form = edit_form(
            initial=initial_data
        )
    else:
        form = edit_form(request.POST)
        if form.is_valid():
            if user_type is AppUser.PROFILE_USER:
                user.first_name = form.cleaned_data['first_name']
            else:
                user.first_name = form.cleaned_data['first_name']
                user.company_name = form.cleaned_data['company_name']
            user.save()

            return redirect('profile_user')

    return render(request, 'app_auth/edit_profile.html', context={'form': form, 'user_type': user_type})


class DeleteProfileView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = AppUser
    template_name = 'app_auth/delete_profile.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.current_user

    def form_valid(self, form):
        images_list = [job.company_logo
                       for job in Job.objects.filter(hr_id=self.request.current_user.pk).all()]
        success_url = self.get_success_url()
        self.object.delete()

        # Close the file handle
        # self.object.company_logo.close()

        for image in images_list:
            path = image.file.name
            # Close the file before delete
            image.close()

            if os.path.exists(path):
                os.remove(path)

        return HttpResponseRedirect(success_url)
