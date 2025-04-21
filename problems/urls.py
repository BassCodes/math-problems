from django.urls import path

from .views import (
    HomePageView,
    AboutPageView,
    ProblemListView,
    ProblemDetailView,
    SourceListView,
    SourceDetailView,
    SourceGroupDetailView,
    problem_list,
)

urlpatterns = [
    path("about/", AboutPageView.as_view(), name="about"),
    path("problems/<int:pk>/", ProblemDetailView.as_view(), name="problem_detail"),
    # path("problems/", ProblemListView.as_view(), name="problem_list"),
    path("problems/", problem_list, name="problem_list"),
    path(
        "sources/group/<int:pk>",
        SourceGroupDetailView.as_view(),
        name="source_group_detail",
    ),
    path("sources/<int:pk>/", SourceDetailView.as_view(), name="source_detail"),
    path("sources/", SourceListView.as_view(), name="source_list"),
    path("", HomePageView.as_view(), name="home"),
]
