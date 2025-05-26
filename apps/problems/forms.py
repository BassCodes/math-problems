from django import forms
from .models import Source, Branch, Technique, Type


class SearchForm(forms.Form):
    source = forms.ModelMultipleChoiceField(queryset=None, required=False)
    branch = forms.ModelMultipleChoiceField(queryset=None, required=False)
    type = forms.ModelMultipleChoiceField(queryset=None, required=False)
    tech = forms.ModelMultipleChoiceField(queryset=None, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["source"].queryset = Source.objects.all()
        self.fields["branch"].queryset = Branch.objects.all()
        self.fields["tech"].queryset = Technique.objects.all()
        self.fields["type"].queryset = Type.objects.all()
