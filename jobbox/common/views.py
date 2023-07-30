from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

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
        except:
            pass

        return initial

