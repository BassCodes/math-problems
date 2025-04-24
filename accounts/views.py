from django.views.generic import TemplateView


class LogoutPageView(TemplateView):
    template_name = "registration/logout.html"
