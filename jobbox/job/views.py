import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins

from jobbox.app_auth.views import check_if_account_is_user_or_hr
from jobbox.job.forms import CreateJobFrom, EditJobFrom
from jobbox.job.models import Job



class CreateJobView(views.CreateView):
    template_name = 'job/create-job.html'
    model = Job
    # fields = ['title', 'company_logo', 'programming_language', 'salary', 'description']
    fields = '__all__'

    success_url = reverse_lazy('index')

    def form_valid(self, form):
        a = self
        super().form_valid(form)

@login_required
def create_job(request):
    user, user_type = check_if_account_is_user_or_hr(request)
    if user_type != 'hr':
        return redirect('index')

    if request.method == 'GET':
        form = CreateJobFrom(initial={'hr': user.pk})
    else:
        form = CreateJobFrom(request.POST, request.FILES)
        if form.is_valid():
            form.fields['hr_id'] = user.pk
            form.save()

            return redirect('profile_user')

    context = {

        'form': form,
    }

    return render(request, 'job/create-job.html', context=context)


class HrJobListView(views.ListView):
    template_name = 'job/hr_job_list.html'
    model = Job

    def get_queryset(self):
        jobs = Job.objects.filter(hr_id=self.request.current_user.pk)
        return jobs


class DescriptionJobView(views.DetailView):
    template_name = 'job/description.html'
    model = Job


class EditJobView(views.UpdateView):
    template_name = 'job/update.html'
    model = Job
    form_class = EditJobFrom

    def get_success_url(self):
        pk = self.object.pk

        return reverse_lazy('description_job', kwargs={'pk': pk})


class DeleteJobView(views.DeleteView):
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

