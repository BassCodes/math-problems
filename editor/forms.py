from django import forms
from django.core.exceptions import ValidationError
import problems


class ProblemForm(forms.ModelForm):
    class Meta:
        model = problems.models.Problem
        fields = ["problem_text","answer_text", "categories", "types","source","number"]
    
    # def clean_number(self):
    #     number = self.cleaned_data["number"]
    #     problem_count = self.cleaned_data["source"].problem_count
    #     if number and problem_count and not (number <= problem_count):
    #         raise ValidationError('Problem number must be within source problem number count.')
    #     return self.cleaned_data

class SolutionForm(forms.ModelForm):
    class Meta:
        model = problems.models.Solution
        fields = ["solution_text", "techniques"]
        exclude = ('problem',)