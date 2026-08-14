from django import forms
from .models import JournalEntry


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ["title", "category","mood", "content"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Journal Title",
            }),
            "category": forms.Select(attrs={
                "class": "form-control",
            }),
            "mood": forms.Select(attrs={
    "class": "form-control",
}),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 8,
                "placeholder": "Write your thoughts here...",
            }),
        }