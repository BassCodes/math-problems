from django.urls import path

from .views import (
    HomePageView,
    problem_detail_view,
    SourceListView,
    SourceDetailView,
    SourceGroupDetailView,
    problem_list_view,
    SourceMissingProblemsView,
)

urlpatterns = [
    path("problems/<int:pk>", problem_detail_view, name="problem_detail"),
    path("problems/", problem_list_view, name="problem_list"),
    path(
        "sources/group/<int:pk>",
        SourceGroupDetailView.as_view(),
        name="source_group_detail",
    ),
    path("sources/<int:pk>/", SourceDetailView.as_view(), name="source_detail"),
    path(
        "sources/<int:pk>/missing",
        SourceMissingProblemsView.as_view(),
        name="missing_problem",
    ),
    path("sources/", SourceListView.as_view(), name="source_list"),
    path("", HomePageView.as_view(), name="home"),
]
