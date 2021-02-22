from django.views.generic.base import View
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.shortcuts import redirect


class LoginView(FormView):
    template_name = 'authentication/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


class RegistrationView(FormView):
    model = User
    template_name = 'authentication/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        login(self.request, form.save())
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect(reverse_lazy('index'))
