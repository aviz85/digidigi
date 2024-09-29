from django.core.management.base import BaseCommand
from core.models import Book

class Command(BaseCommand):
    help = 'Regenerates thumbnails for all books'

    def handle(self, *args, **options):
        books = Book.objects.all()
        for book in books:
            if book.cover:
                # Access the thumbnail to force its generation
                book.cover_thumbnail.generate()
                self.stdout.write(self.style.SUCCESS(f'Regenerated thumbnail for "{book.title}"'))

        self.stdout.write(self.style.SUCCESS('Finished regenerating all thumbnails'))