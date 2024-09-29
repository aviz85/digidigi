import os
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from core.models import Book

class Command(BaseCommand):
    help = 'Downloads book covers from URLs and associates them with Book models'

    def handle(self, *args, **options):
        books = Book.objects.filter(cover__isnull=True)
        for book in books:
            if not book.cover:
                # Replace this URL with a real image URL for each book
                image_url = f"https://picsum.photos/200/300?random={book.id}"
                
                # Download the image
                response = requests.get(image_url)
                if response.status_code == 200:
                    # Create a temporary file
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(response.content)
                    img_temp.flush()

                    # Save the image to the book's cover field
                    file_name = f"book_cover_{book.id}.jpg"
                    book.cover.save(file_name, File(img_temp), save=True)
                    
                    self.stdout.write(self.style.SUCCESS(f'Successfully downloaded cover for "{book.title}"'))
                else:
                    self.stdout.write(self.style.ERROR(f'Failed to download cover for "{book.title}"'))

        self.stdout.write(self.style.SUCCESS('Finished downloading book covers'))