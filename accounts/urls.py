from django.urls import path

from .views import LogoutPageView, UserProfileView, UserOwnProfileView

urlpatterns = [
    path("<uuid:pk>", UserProfileView.as_view(), name="user_profile"),
    path("logged-out/", LogoutPageView.as_view(), name="logout-page"),
    path("my-profile/", UserOwnProfileView.as_view(), name="my_profile"),
]
