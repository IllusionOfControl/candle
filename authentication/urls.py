from django.urls import path
from django.contrib.auth.views import LogoutView
from authentication.views import LoginView, RegistrationView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration')
]
