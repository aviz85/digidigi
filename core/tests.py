from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Book, Author
from django.utils import timezone
import os
from django.conf import settings
from PIL import Image
import io

class BookModelTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            isbn="1234567890123",
            publication_date=timezone.now().date(),
            genre="Test Genre",
            available_copies=5
        )

    def test_book_creation(self):
        self.assertTrue(isinstance(self.book, Book))
        self.assertEqual(self.book.__str__(), self.book.title)

    def test_book_fields(self):
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(self.book.isbn, "1234567890123")
        self.assertEqual(self.book.genre, "Test Genre")
        self.assertEqual(self.book.available_copies, 5)

class BookViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            author=self.author,
            isbn="1234567890123",
            publication_date=timezone.now().date(),
            genre="Test Genre",
            available_copies=5
        )
        self.book_list_url = reverse('core:book_list')
        self.book_detail_url = reverse('core:book_detail', args=[self.book.id])

    def test_book_list_view(self):
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/book_list.html')
        self.assertContains(response, self.book.title)

    def test_book_detail_view(self):
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/book_detail.html')
        self.assertContains(response, self.book.title)
        self.assertContains(response, self.book.author.name)
        self.assertContains(response, self.book.isbn)

    def test_book_list_view_no_books(self):
        Book.objects.all().delete()
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No books available")

    def test_book_detail_view_invalid_id(self):
        invalid_detail_url = reverse('core:book_detail', args=[999])  # Assuming 999 is an invalid ID
        response = self.client.get(invalid_detail_url)
        self.assertEqual(response.status_code, 404)

class BookCoverTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        
        # Create a dummy image file for testing
        image = Image.new('RGB', (100, 100), color='red')
        img_io = io.BytesIO()
        image.save(img_io, format='JPEG')
        img_content = img_io.getvalue()
        
        self.book_with_cover = Book.objects.create(
            title="Book With Cover",
            author=self.author,
            isbn="1234567890123",
            publication_date=timezone.now().date(),
            genre="Test Genre",
            available_copies=5,
            cover=SimpleUploadedFile("test_cover.jpg", img_content, content_type="image/jpeg")
        )
        self.book_without_cover = Book.objects.create(
            title="Book Without Cover",
            author=self.author,
            isbn="3210987654321",
            publication_date=timezone.now().date(),
            genre="Test Genre",
            available_copies=3
        )

    def test_book_with_cover(self):
        self.assertTrue(self.book_with_cover.has_cover)
        self.assertIsNotNone(self.book_with_cover.cover_thumbnail_url)

    def test_book_without_cover(self):
        self.assertFalse(self.book_without_cover.has_cover)
        self.assertIsNone(self.book_without_cover.cover_thumbnail_url)

    def test_book_list_view_with_cover(self):
        response = self.client.get(reverse('core:book_list'))
        self.assertContains(response, 'img src=')
        self.assertContains(response, 'Book With Cover')
        self.assertContains(response, 'Book Without Cover')

    def test_book_detail_view_with_cover(self):
        book = self.book_with_cover
        print(f"Book ID: {book.id}")
        print(f"Book title: {book.title}")
        print(f"Has cover: {book.has_cover}")
        print(f"Cover URL: {book.cover.url if book.cover else 'No cover'}")
        
        response = self.client.get(reverse('core:book_detail', args=[book.id]))
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content.decode()}")
        
        self.assertContains(response, 'img class=')
        self.assertContains(response, book.cover.url)
        self.assertContains(response, book.title)

    def test_book_detail_view_without_cover(self):
        response = self.client.get(reverse('core:book_detail', args=[self.book_without_cover.id]))
        self.assertNotContains(response, 'img src=')
        self.assertContains(response, 'Book Without Cover')