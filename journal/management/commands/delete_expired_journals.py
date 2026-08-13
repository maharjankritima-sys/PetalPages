from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from journal.models import JournalEntry


class Command(BaseCommand):

    help = "Permanently delete journals that have been in trash for more than 10 days."

    def handle(self, *args, **kwargs):

        expiry_date = timezone.now() - timedelta(days=10)

        expired_journals = JournalEntry.objects.filter(
            deleted_at__isnull=False,
            deleted_at__lte=expiry_date
        )

        count = expired_journals.count()

        expired_journals.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f"{count} journal(s) permanently deleted."
            )
        )