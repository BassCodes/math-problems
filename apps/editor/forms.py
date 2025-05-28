from django import forms
import problems


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


class SolutionForm(forms.ModelForm):
    class Meta:
        model = problems.models.Solution
        fields = [
            "solution_text",
            # "techniques"
        ]
        exclude = ("problem",)
