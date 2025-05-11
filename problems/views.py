from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q,F
from django.shortcuts import get_object_or_404
from .models import Problem, Branch, Technique, Source, SourceGroup, Solution, Type
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden
from django.shortcuts import redirect
import json


class HomePageView(TemplateView):
    template_name = "home.html"


def problem_list_view(request):
    # Filters for source, branch, and technique are sent in the url search
    # parameter in the following format: "?sou=[1,2]&cat=[8,3]"
    # where "sou" -> "source" and the list after the equals contains a list
    # of ids for the respective model to filter by
    try:
        sources_query_request = json.loads(request.GET.get("sou", "[]"))
        branch_query_request = json.loads(request.GET.get("cat", "[]"))
        technique_query_request = json.loads(request.GET.get("tec", "[]"))
    except json.JSONDecodeError:
        return redirect(problem_list_view)

    # Create a Q-query object to contain filter
    final_query = Q()

    # Add source filter to final query
    # Sources are filtered by union, e.g. a source can pass the filter when it
    # matches any one of the requested ids.
    tq = Q()
    for sid in sources_query_request:
        tq |= Q(source__exact=sid)
    final_query &= tq

    # Add branch filter to final query
    # Categories are filtered by intersection, e.g. a branch can pass the filter when it
    # matches *ALL* of the requested ids.
    tq = Q()
    for item in branch_query_request:
        tq |= ~Q(categories__id=item)
    final_query &= ~tq

    # Add Technique filter to final query
    # Techniques are filtered by intersection
    # TODO, broke this
    # tq = Q()
    # for item in technique_query_request:
    #     tq |= ~Q(techniques__id=item)
    # final_query &= ~tq

    # Technique.objects.filter(pk__in=self.solutions.all().values("techniques"))
    # Filter problems
    problems = Problem.objects.filter(final_query).distinct()
    print(problems.query)
    # FUTURE WORK: Only show categories and techniques which are within the
    # filtered `problems` variable

    context = {}
    context["sources_active"] = sources_query_request
    context["categories_active"] = branch_query_request
    context["techniques_active"] = technique_query_request
    context["problems"] = problems.order_by("source", "number")
    context["sources"] = Source.objects.all()
    context["categories"] = Branch.objects.all()
    context["type"] = Type.objects.all()
    context["techniques"] = Technique.objects.all()
    return render(request, "problem_list.html", context)


def problem_detail_view(request, pk):
    problem = get_object_or_404(Problem, pk=pk)
    if not problem.is_published() and not request.user.is_authenticated:
        return HttpResponseForbidden(
            "This problem is a draft. Only logged-in users can view it."
        )

    context = {}
    context["problem"] = problem
    return render(request, "problem.html", context)


class SourceListView(ListView):
    model = Source
    template_name = "source_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["source_list"] = Source.objects.all().order_by("parent").reverse()
        return context


class SourceDetailView(DetailView):
    model = Source
    template_name = "source.html"


class SourceGroupDetailView(DetailView):
    model = SourceGroup
    template_name = "source_group.html"
