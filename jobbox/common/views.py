from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views
from django.contrib.auth import mixins as auth_mixins
from django.core.exceptions import PermissionDenied

from jobbox.common.forms import ContactUsFrom
from jobbox.common.models import ContactUs
from jobbox.job.models import Job


def index(request):
    jobs = Job.objects.all()
    context = {
        'jobs': jobs
    }
    return render(request, 'common/index.html', context=context)


class AboutView(SuccessMessageMixin, views.CreateView):
    template_name = 'common/about.html'
    model = ContactUs
    form_class = ContactUsFrom
    success_url = reverse_lazy('about')
    success_message = "Your message has been sent successfully!"

    def get_initial(self):
        initial = super().get_initial()
        try:
            user_email = self.request.current_user.email
            initial['email'] = user_email
        except AttributeError:
            pass

        return initial


class AdminOrStaffMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_staff:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied()


class ContactUsList(AdminOrStaffMixin, auth_mixins.LoginRequiredMixin, views.ListView):
    template_name = 'common/contact_us_list.html'
    model = ContactUs
    fields = '__all__'


class EditContactUs(AdminOrStaffMixin, auth_mixins.LoginRequiredMixin, views.UpdateView):
    template_name = 'common/edit_contact_us.html'
    model = ContactUs
    form_class = ContactUsFrom
    success_url = reverse_lazy('contact_us_list')


class DeleteContactUs(AdminOrStaffMixin, auth_mixins.LoginRequiredMixin, views.DeleteView):
    template_name = 'common/delete_contact_us.html'
    model = ContactUs
    success_url = reverse_lazy('contact_us_list')

