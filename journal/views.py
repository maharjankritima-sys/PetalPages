from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import JournalEntry, JournalMedia
from .forms import JournalEntryForm


@login_required
def dashboard(request):

    # Get only active journals
    journals = JournalEntry.objects.filter(
        owner=request.user,
        deleted_at__isnull=True
    )

    # Search
    search = request.GET.get("search", "").strip()

    if search:
        journals = journals.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search)
        )

    # Category filter
    category = request.GET.get("category", "").strip()

    if category:
        journals = journals.filter(
            category=category
        )

    # Favorites filter
    favorite = request.GET.get("favorite")

    if favorite == "true":
        journals = journals.filter(
            is_favorite=True
        )

    # Order newest first
    journals = journals.order_by("-created_at")

    # Mood summary
    mood_stats = (
        JournalEntry.objects.filter(
            owner=request.user,
            deleted_at__isnull=True
        )
        .values("mood")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    # Total active journals
    total_journals = JournalEntry.objects.filter(
        owner=request.user,
        deleted_at__isnull=True
    ).count()

    # Total favorite journals
    favorite_count = JournalEntry.objects.filter(
        owner=request.user,
        deleted_at__isnull=True,
        is_favorite=True
    ).count()

    return render(
        request,
        "journal/dashboard.html",
        {
            "journals": journals,
            "search": search,
            "category": category,
            "favorite": favorite,
            "mood_stats": mood_stats,
            "total_journals": total_journals,
            "favorite_count": favorite_count,
        }
    )


@login_required
def toggle_favorite(request, journal_id):

    journal = get_object_or_404(
        JournalEntry,
        id=journal_id,
        owner=request.user,
        deleted_at__isnull=True
    )

    journal.is_favorite = not journal.is_favorite
    journal.save()

    return redirect("journal_dashboard")


@login_required
def create_journal(request):

    if request.method == "POST":

        form = JournalEntryForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            # Save journal
            journal = form.save(commit=False)
            journal.owner = request.user
            journal.save()

            # Get all uploaded photos/videos
            files = request.FILES.getlist("media")

            # Save each media file
            for uploaded_file in files:

                JournalMedia.objects.create(
                    journal=journal,
                    file=uploaded_file
                )

            return redirect(
                "journal_detail",
                journal.id
            )

    else:

        form = JournalEntryForm()

    return render(
        request,
        "journal/create.html",
        {
            "form": form
        }
    )
@login_required
def journal_detail(request, journal_id):

    journal = get_object_or_404(
        JournalEntry,
        id=journal_id,
        owner=request.user
    )

    return render(
        request,
        "journal/detail.html",
        {
            "journal": journal
        }
    )


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
            request.FILES,
            instance=journal
        )

        if form.is_valid():

            form.save()

            # Add newly uploaded photos/videos
            files = request.FILES.getlist("media")

            for uploaded_file in files:

                JournalMedia.objects.create(
                    journal=journal,
                    file=uploaded_file
                )

            return redirect(
                "journal_detail",
                journal.id
            )

    else:

        form = JournalEntryForm(
            instance=journal
        )

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
        owner=request.user,
        deleted_at__isnull=True
    )

    # Soft delete
    journal.deleted_at = timezone.now()
    journal.save()

    return redirect("journal_dashboard")


@login_required
def trash(request):

    deleted_journals = JournalEntry.objects.filter(
        owner=request.user,
        deleted_at__isnull=False
    ).order_by("-deleted_at")

    return render(
        request,
        "journal/trash.html",
        {
            "deleted_journals": deleted_journals,
        }
    )


@login_required
def delete_permanently(request, journal_id):

    journal = get_object_or_404(
        JournalEntry,
        id=journal_id,
        owner=request.user,
        deleted_at__isnull=False
    )

    # Permanently delete from PostgreSQL
    journal.delete()

    return redirect("trash")
@login_required
def restore_journal(request, journal_id):

    journal = get_object_or_404(
        JournalEntry,
        id=journal_id,
        owner=request.user,
        deleted_at__isnull=False
    )

    journal.deleted_at = None
    journal.save()

    return redirect("trash")
@login_required
def profile(request):

    total_journals = JournalEntry.objects.filter(
        owner=request.user,
        deleted_at__isnull=True
    ).count()

    favorite_count = JournalEntry.objects.filter(
        owner=request.user,
        deleted_at__isnull=True,
        is_favorite=True
    ).count()

    return render(
        request,
        "journal/profile.html",
        {
            "total_journals": total_journals,
            "favorite_count": favorite_count,
        }
    )
@login_required
def delete_media(request, media_id):

    media = get_object_or_404(
        JournalMedia,
        id=media_id,
        journal__owner=request.user
    )

    journal_id = media.journal.id

    media.file.delete(save=False)
    media.delete()

    return redirect(
        "edit_journal",
        journal_id
    )