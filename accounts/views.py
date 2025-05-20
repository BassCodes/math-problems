from django.views.generic import TemplateView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from .models import CustomUser
from .forms import CustomAuthenticationForm, CustomUserCreationForm


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class LogoutPageView(TemplateView):
    template_name = "registration/logout.html"


class UserProfileView(DetailView):
    model = CustomUser
    template_name = "profile/user_profile.html"


class UserOwnProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "profile/user_profile.html"

    def get_object(self, queryset=None):
        return self.request.user
