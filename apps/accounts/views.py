from django.views.generic import TemplateView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.http import HttpResponseBadRequest

from .models import CustomUser
from .forms import CustomAuthenticationForm, CustomUserCreationForm


# modified from LoginRequiredMixin
class LoginImpermissibleMixin(AccessMixin):
    """Verify that the current user is not authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseBadRequest("This can not be accessed while logged in")
        return super().dispatch(request, *args, **kwargs)


class CustomLoginView(LoginImpermissibleMixin, LoginView):
    authentication_form = CustomAuthenticationForm


class SignUpView(LoginImpermissibleMixin, CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class LogoutPageView(LoginRequiredMixin, TemplateView):
    template_name = "registration/logout.html"


class UserProfileView(DetailView):
    model = CustomUser
    template_name = "profile/user_profile.html"


class UserOwnProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "profile/user_profile.html"

    def get_object(self, queryset=None):
        return self.request.user
