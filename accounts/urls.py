from django.urls import path

from .views import LogoutPageView,UserProfileView

urlpatterns = [
    path("profile/<int:pk>", UserProfileView.as_view(), name="user-profile"),
    path("logged-out/", LogoutPageView.as_view(), name="logout-page"),
]
