from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import JournalEntry
from .forms import JournalEntryForm


@login_required
def dashboard(request):

    journals = JournalEntry.objects.filter(
        owner=request.user
    )

    search = request.GET.get("search")

    if search:
        journals = journals.filter(
            title__icontains=search
        ) | journals.filter(
            content__icontains=search
        )

    journals = journals.order_by("-created_at")

    return render(
        request,
        "journal/dashboard.html",
        {
            "journals": journals,
            "search": search,
        }
    )


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


@login_required
def journal_detail(request, journal_id):

    journal = get_object_or_404(
        JournalEntry,
        id=journal_id,
        owner=request.user
    )

    return render(request, "journal/detail.html", {
        "journal": journal
    })


@login_required
def edit_journal(request, journal_id):

    journal = get_object_or_404(
        JournalEntry,
        id=journal_id,
        owner=request.user
    )

    if request.method == "POST":

        form = JournalEntryForm(
            request.POST,
            instance=journal
        )

        if form.is_valid():
            form.save()
            return redirect("journal_detail", journal.id)

    else:

        form = JournalEntryForm(instance=journal)

    return render(
        request,
        "journal/edit.html",
        {
            "form": form,
            "journal": journal,
        }
    )
@login_required
def delete_journal(request, journal_id):

    journal = get_object_or_404(
        JournalEntry,
        id=journal_id,
        owner=request.user
    )

    if request.method == "POST":
        journal.delete()
        return redirect("journal_dashboard")

    return render(
        request,
        "journal/delete.html",
        {
            "journal": journal,
        }
    )