from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import JournalEntry
from .forms import JournalEntryForm


@login_required
def dashboard(request):
    journals = JournalEntry.objects.filter(owner=request.user).order_by("-created_at")

    return render(request, "journal/dashboard.html", {
        "journals": journals
    })


@login_required
def create_journal(request):

    if request.method == "POST":

        form = JournalEntryForm(request.POST)

        if form.is_valid():
            journal = form.save(commit=False)
            journal.owner = request.user
            journal.save()

            return redirect("journal_dashboard")

    else:
        form = JournalEntryForm()

    return render(request, "journal/create.html", {
        "form": form
    })