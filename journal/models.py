from django.db import models
from django.contrib.auth.models import User


class JournalEntry(models.Model):

    CATEGORY_CHOICES = [
        ("personal", "Personal"),
        ("study", "Study"),
        ("memories", "Memories"),
        ("goals", "Goals"),
        ("other", "Other"),
    ]

    MOOD_CHOICES = [
        ("happy", "😊 Happy"),
        ("calm", "😌 Calm"),
        ("loved", "🥰 Loved"),
        ("sad", "😢 Sad"),
        ("angry", "😡 Angry"),
        ("anxious", "😰 Anxious"),
        ("tired", "😴 Tired"),
    ]

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="journals"
    )

    title = models.CharField(max_length=200)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="personal"
    )

    mood = models.CharField(
        max_length=20,
        choices=MOOD_CHOICES,
        default="happy"
    )

    is_favorite = models.BooleanField(default=False)

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class JournalMedia(models.Model):

    journal = models.ForeignKey(
        JournalEntry,
        on_delete=models.CASCADE,
        related_name="media"
    )

    file = models.FileField(
        upload_to="journal_media/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Media for {self.journal.title}"