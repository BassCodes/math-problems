from django.shortcuts import render
from django.views.generic import DetailView

from problems.models import Problem


class ProblemHistoryView(DetailView):
    model = Problem
    template_name = "history/problem_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        problem = context["problem"]

        diffs = []
        last_hist = None
        for hist in problem.history.all():
            print(hist)
            if last_hist is None:
                diffs.append({"history": hist, "diff": None})
            else:
                diffs.append(
                    {
                        "history": hist,
                        "diff": last_hist.diff_against(hist).changed_fields,
                    }
                )
            last_hist = hist

        context["diffs"] = diffs

        return context
