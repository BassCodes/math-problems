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
    path(
        "problem/<slug:slug>/<int:number>", problem_detail_view, name="problem_detail"
    ),
    path("problem/<int:pk>", problem_detail_view, name="problem_detail"),
    path("problem/", problem_list_view, name="problem_list"),
    path(
        "source/group/<int:pk>",
        SourceGroupDetailView.as_view(),
        name="source_group_detail",
    ),
    path("source/<slug:slug>/", SourceDetailView.as_view(), name="source_detail"),
    path(
        "source/<int:pk>/missing",
        SourceMissingProblemsView.as_view(),
        name="missing_problem",
    ),
    path("source/", SourceListView.as_view(), name="source_list"),
    path("", HomePageView.as_view(), name="home"),
]
