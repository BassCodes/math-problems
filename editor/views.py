from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

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
        # FUTURE WORK: Add drafts system
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


class EditorProblemDeleteView(LoginRequiredMixin, DeleteView):
    model = problems.models.Problem
    template_name = "editor/problem_confirm_delete.html"
    success_url = reverse_lazy("editor_home")
