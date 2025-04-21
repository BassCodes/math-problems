from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q

from .models import Problem, Category, Technique, Source, SourceGroup

import json


class HomePageView(TemplateView):
    template_name = "home.html"


class AboutPageView(TemplateView):
    template_name = "about.html"


class ProblemListView(ListView):
    model = Problem
    template_name = "problem_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sources"] = Source.objects.all().order_by("shortname", "name")
        context["categories"] = Category.objects.all()
        context["techniques"] = Technique.objects.all()
        return context


def problem_list(request):
    print(request.GET)
    sources_query_request = json.loads(request.GET.get("sou", "[]"))

    final_query = Q()

    tq = Q()
    for sid in sources_query_request:
        tq |= Q(source__exact=sid)
    final_query &= tq

    problems = Problem.objects.all().filter(final_query)

    context = {}
    context["sources_active"] = sources_query_request
    context["problems"] = problems
    context["sources"] = Source.objects.all().order_by("shortname", "name")
    context["categories"] = Category.objects.all()
    context["techniques"] = Technique.objects.all()
    return render(request, "problem_list.html", context)


class ProblemDetailView(DetailView):
    model = Problem
    template_name = "problem.html"


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


def source_detail(request):
    sources = Source.objects.exclude(parent__isnull=False)
    groups = SourceGroup.objects.all()
    context = {"sources": sources, "groups": groups}
    return render(request, "view_item.html", context)
