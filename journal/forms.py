from django import forms
from .models import JournalEntry


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ["title", "content"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Journal Title",
            }),

            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 8,
                "placeholder": "Write your thoughts here...",
            }),
        }