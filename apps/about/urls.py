from django.urls import path

from .views import (
    AboutPageView,
    CopyrightPageView,
    OpenSourceLicensePageView,
    StyleGuidePageView,
)

urlpatterns = [
    path("", AboutPageView.as_view(), name="about_page"),
    path("copyright", CopyrightPageView.as_view(), name="copyright_page"),
    path("open-source", OpenSourceLicensePageView.as_view(), name="open_source_page"),
    path("style-guide", StyleGuidePageView.as_view(), name="style_guide_page"),
]
