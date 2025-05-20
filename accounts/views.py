from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import CustomUser


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
