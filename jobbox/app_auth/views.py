import os

from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import views as auth_views
from django.contrib.auth import mixins as auth_mixins
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from jobbox.app_auth.forms import RegisterUserHRForm, EditUserHRForm, UserLoginForm, UserChangePasswordForm, \
    AdminChangeEmailForm
from jobbox.app_auth.models import AppUser
from jobbox.common.models import ProfileHR

from jobbox.job.models import Job, UploadCV
from jobbox.task.models import HRTask

UserModel = get_user_model()


class LoginUserView(auth_views.LoginView):
    template_name = 'app_auth/login.html'
    authentication_form = UserLoginForm


class RegisterUserView(views.CreateView):
    template_name = 'app_auth/register.html'
    form_class = RegisterUserHRForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)

        return result


class LogoutUserView(auth_views.LogoutView):
    pass


@login_required
def profile_user(request):
    context = {
        'user': request.current_user,
        'number_of_tasks': len(HRTask.objects.filter(user_id=request.current_user.pk)),
        'number_of_jobs': len(Job.objects.filter(hr=request.current_user.pk)),
    }
    return render(request, 'app_auth/profile.html', context=context)


@login_required
def update_profile(request):
    user = request.current_user.profilehr

    # Set the initial data for edit in the form
    initial_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'company_name': user.company_name,
        'profile_picture': user.profile_picture,
        'telephone_number': user.telephone_number,
    }

    if request.method == 'GET':
        form = EditUserHRForm(
            initial=initial_data
        )
    else:
        form = EditUserHRForm(request.POST, request.FILES)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.company_name = form.cleaned_data['company_name']
            user.telephone_number = form.cleaned_data['telephone_number']

            if 'profile_picture' in form.cleaned_data:
                if form.cleaned_data['profile_picture'] is not None:
                    new_profile_picture = form.cleaned_data['profile_picture']
                    # Check if the new profile picture is different from the existing one
                    if new_profile_picture != user.profile_picture:
                        # Remove the existing profile picture file from storage
                        if user.profile_picture:
                            # Delete the existing profile picture file from storage
                            if os.path.exists(user.profile_picture.path):
                                os.remove(user.profile_picture.path)
                        # Assign the new profile picture to the user
                        user.profile_picture = new_profile_picture

            user.save()

            return redirect('profile_user')

    return render(request, 'app_auth/edit_profile.html', context={'form': form, 'user': user})


@login_required
def change_password(request):
    if request.method == "GET":
        form = UserChangePasswordForm(request.user)
    else:
        form = UserChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            login(request, request.user)
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('profile_user')

    context = {
        'form': form,
    }

    return render(request, 'app_auth/change_password.html', context=context)


class DeleteProfileView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = AppUser
    template_name = 'app_auth/delete_profile.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.current_user

    def form_valid(self, form):
        user = self.request.current_user
        files_list = [job.company_logo
                       for job in Job.objects.filter(hr_id=user.pk).all()]

        all_user_jobs = Job.objects.filter(hr_id=user.pk)
        all_cvs = UploadCV.objects.all()

        for user_job in all_user_jobs:
            for cv in all_cvs:
                if user_job.pk == cv.job_id_id:
                    files_list.append(cv.pdf_file)

        # Check if there is profile picture and then add it to the list
        if user.profilehr.profile_picture:
            files_list.append(user.profilehr.profile_picture)

        success_url = self.get_success_url()
        self.object.delete()

        for image in files_list:
            if hasattr(image, 'file'):
                path = image.file.name
                # Close the file before delete
                image.close()

            if os.path.exists(path):
                os.remove(path)

        return HttpResponseRedirect(success_url)


class AdminOrStaffMixin:
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.is_staff):
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class AdminMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)


class AllProfiles(auth_mixins.LoginRequiredMixin, AdminOrStaffMixin, views.ListView):
    template_name = 'app_auth/all_profiles.html'
    model = ProfileHR
    form_class = EditUserHRForm
    success_url = reverse_lazy('all_profiles')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accounts'] = UserModel.objects.all()
        return context


class EditProfileAdministrator(auth_mixins.LoginRequiredMixin, AdminOrStaffMixin, views.UpdateView):
    template_name = 'app_auth/edit_profile.html'
    model = ProfileHR
    form_class = EditUserHRForm
    success_url = reverse_lazy('all_profiles')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['administrator'] = True
        return context


class ChangeEmailAndRightsAdministrator(auth_mixins.LoginRequiredMixin, AdminMixin, views.UpdateView):
    template_name = 'app_auth/change_email_and_rights_administration.html'
    model = UserModel
    form_class = AdminChangeEmailForm
    success_url = reverse_lazy('all_profiles')


class DeleteProfileAdministrator(auth_mixins.LoginRequiredMixin, AdminMixin, views.DeleteView):
    template_name = 'app_auth/delete_profile.html'
    model = AppUser
    success_url = reverse_lazy('all_profiles')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['administrator'] = True
        return context

    def form_valid(self, form):
        user = self.object
        files_list = [job.company_logo for job in Job.objects.filter(hr_id=user.pk).all()]
        all_user_jobs = Job.objects.filter(hr_id=user.pk)
        all_cvs = UploadCV.objects.all()

        for user_job in all_user_jobs:
            for cv in all_cvs:
                if user_job.pk == cv.job_id_id:
                    files_list.append(cv.pdf_file)

        # Check if there is profile picture and then add it to the list
        if user.profilehr.profile_picture:
            files_list.append(user.profilehr.profile_picture)

        success_url = self.get_success_url()
        self.object.delete()

        for image in files_list:
            if hasattr(image, 'file'):
                path = image.file.name
                # Close the file before delete
                image.close()

            if os.path.exists(path):
                os.remove(path)

        return HttpResponseRedirect(success_url)
