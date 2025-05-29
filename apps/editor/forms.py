from django import forms
import problems
from .models import DraftSource, DraftProblem


class ProblemForm(forms.ModelForm):
    class Meta:
        model = problems.models.Problem
        fields = [
            "problem_text",
            "has_answer",
            "answer_text",
            # "branches",
            # "types",
            "source",
            "number",
        ]

    def clean_answer_text(self):
        # If the has_answer boolean is false, get rid of any answer data.

        if not self.cleaned_data.get("has_answer"):
            return ""
        else:
            return self.cleaned_data["answer_text"]


class SourceForm(forms.ModelForm):
    class Meta:
        model = DraftSource
        fields = [
            "name",
            "shortname",
            "subtitle",
            "parent",
            "problem_count",
            "description",
            "publish_date",
            "url",
        ]


class SolutionForm(forms.ModelForm):
    class Meta:
        model = problems.models.Solution
        fields = ["solution_text"]
        exclude = ("problem",)
