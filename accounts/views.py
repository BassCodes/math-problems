from django.views.generic import TemplateView, DetailView

from .models import CustomUser


class LogoutPageView(TemplateView):
    template_name = "registration/logout.html"


class UserProfileView(DetailView):
    model = CustomUser
    template_name = "profile/user_profile.html"
