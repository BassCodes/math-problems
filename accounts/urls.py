from django.urls import path

from .views import (
    LogoutPageView,
    UserProfileView,
    UserOwnProfileView,
    CustomLoginView,
    SignUpView,
)

urlpatterns = [
    path("<uuid:pk>", UserProfileView.as_view(), name="user_profile"),
    path("logged-out/", LogoutPageView.as_view(), name="logout-page"),
    path("login/", CustomLoginView.as_view(), name="login_page"),
    path("signup", SignUpView.as_view(), name="signup_page"),
    path("my-profile/", UserOwnProfileView.as_view(), name="my_profile"),
]
