from django import forms
from .models import Journey

# define and create form
class JourneyForm(forms.ModelForm):
    class Meta:
        model = Journey
        fields = ["query_from", "query_to", "icscode_from", "icscode_to", "commonname_from", "commonname_to"]
