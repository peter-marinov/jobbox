from django.contrib.auth import login

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as view
from django.contrib.auth import views as auth_views

from jobbox.app_auth.forms import RegisterUserForm, RegisterUserHRForm


class LoginUserView(auth_views.LoginView):
    template_name = 'app_auth/login.html'


class RegisterUserView(view.CreateView):
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


class RegisterHRView(view.CreateView):
    template_name = 'app_auth/register.html'
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

