import os

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.contrib import messages
from django.http import FileResponse
from django.core.exceptions import PermissionDenied

from jobbox.app_auth.views import check_if_account_is_user_or_hr
from jobbox.job.forms import CreateJobFrom, EditJobFrom, UploadCVForm
from jobbox.job.models import Job, UploadCV


@login_required
def create_job(request):
    user = check_if_account_is_user_or_hr(request)

    if request.method == 'GET':
        form = CreateJobFrom(initial={'hr': user.pk})
    else:
        form = CreateJobFrom(request.POST, request.FILES)
        if form.is_valid():
            form.fields['hr_id'] = user.pk
            form.save()

            return redirect('my_hr_list')

    context = {

        'form': form,
    }

    return render(request, 'job/create_job.html', context=context)


class HrJobListView(views.ListView):
    template_name = 'job/hr_job_list.html'
    model = Job

    def get_queryset(self):
        jobs = Job.objects.filter(hr_id=self.request.current_user.pk)
        return jobs

    def dispatch(self, request, *args, **kwargs):
        user = self.request.current_user

        if hasattr(user, 'profilehr') or user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied()


def description_job_view(request, pk):
    job_object =  get_object_or_404(Job, pk=pk)
    job_cvs = UploadCV.objects.filter(job_id=pk)
    if request.method == 'GET':
        form = UploadCVForm(initial={'job_id': job_object.pk})
    else:
        form = UploadCVForm(request.POST, request.FILES)
        if form.is_valid():
            form.fields['job_id'] = job_object.pk
            form.save()

            messages.success(request, 'File uploaded successfully.')

            return redirect('description_job', pk=pk)

    context = {
        'form': form,
        'object': job_object,
        'job_cvs': job_cvs,
    }

    return render(request, 'job/description_job.html', context=context)


def download_cv(request, pk):
    cv_object = get_object_or_404(UploadCV, pk=pk)
    cv_path = cv_object.pdf_file.path
    cv_name = cv_object.pdf_file.name.split('/')[-1]

    # Open the CV file using FileResponse and serve it for download
    response = FileResponse(open(cv_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{cv_name}"'
    return response


class OnlyHRCanEditAndDeleteTheirJobMixin:
    def dispatch(self, request, *args, **kwargs):
        user = self.request.current_user
        if not user:
            raise PermissionDenied()

        try:
            job = Job.objects.get(pk=kwargs['pk'])
            if job.hr_id == user.pk:
                has_job_created = job
            else:
                has_job_created = None
        except Job.DoesNotExist:
            has_job_created = None

        if hasattr(user, 'profilehr') and has_job_created:
            return super().dispatch(request, *args, **kwargs)

        raise PermissionDenied()


class EditJobView(OnlyHRCanEditAndDeleteTheirJobMixin, views.UpdateView):
    template_name = 'job/edit_job.html'
    model = Job
    form_class = EditJobFrom

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('description_job', kwargs={'pk': pk})

    def form_valid(self, form):
        if 'company_logo' in form.cleaned_data:
            new_company_logo = form.cleaned_data['company_logo']
            job = Job.objects.get(pk=self.kwargs['pk'])

            # Check if the new logo picture is different from the existing one
            if new_company_logo != job.company_logo:
                # Check if there is company logo
                if job.company_logo:
                    # Delete the existing profile picture file from storage
                    if os.path.exists(job.company_logo.path):
                        os.remove(job.company_logo.path)

                # Assign the new logo picture to the job
                job.company_logo = new_company_logo

        self.object = form.save()
        return super().form_valid(form)



class DeleteJobView(OnlyHRCanEditAndDeleteTheirJobMixin, views.DeleteView):
    template_name = 'job/delete_job.html'
    model = Job

    success_url = reverse_lazy('profile_user')

    def form_valid(self, form):
        path = self.object.company_logo.file.name
        success_url = self.get_success_url()
        self.object.delete()

        # Close the file handle
        self.object.company_logo.close()

        if os.path.exists(path):
            os.remove(path)
        return HttpResponseRedirect(success_url)


class DeleteCVView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    template_name = 'job/delete_cv.html'
    model = UploadCV
    fields = '__all__'
    success_message = 'The CV has been removed successfully.'
    success_url = reverse_lazy('profile_user')