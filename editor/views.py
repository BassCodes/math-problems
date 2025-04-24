from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin

import datetime
import problems


class EditorHomePageView(LoginRequiredMixin, TemplateView):
    template_name = "editor/editor_home.html"


class EditorCreateProblemView(LoginRequiredMixin, CreateView):
    model = problems.models.Problem

    template_name = "editor/create_problem.html"
    fields = [
        "source",
        "number",
        "problem_text",
        "solution_text",
        "answer_text",
        "categories",
        "techniques",
    ]

    def form_valid(self, form):
        form.instance.pub_date = datetime.date.today()
        form.instance.contributor = self.request.user
        return super().form_valid(form)


class EditorUpdateProblemView(LoginRequiredMixin, UpdateView):
    model = problems.models.Problem
    template_name = "editor/edit_problem.html"
    fields = (
        "problem_text",
        "solution_text",
        "answer_text",
        "source",
        "number",
        "categories",
        "techniques",
    )
