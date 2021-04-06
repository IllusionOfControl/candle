from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView


class LoginView(LoginView):
    template_name = 'authentication/login.html'


class RegistrationView(FormView):
    model = User
    template_name = 'authentication/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        login(self.request, form.save())
        return super().form_valid(form)
