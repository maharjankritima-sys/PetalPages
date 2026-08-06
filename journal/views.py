from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import JournalEntryForm




@login_required
def dashboard(request):
    return render(request, "journal/dashboard.html")
@login_required
def create_journal(request):

    if request.method == "POST":

        form = JournalEntryForm(request.POST)

        if form.is_valid():

            journal = form.save(commit=False)
            journal.owner = request.user
            journal.save()

            return redirect("home")

    else:

        form = JournalEntryForm()

    return render(request, "journal/create.html", {
        "form": form
    })