from django.urls import path

from .views import LogoutPageView

urlpatterns = [
    path("logged-out/", LogoutPageView.as_view(), name="logout-page"),
]
