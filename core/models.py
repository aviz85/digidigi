from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

class Author(models.Model):
    name = models.CharField(max_length=200)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publication_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=100)
    available_copies = models.PositiveIntegerField(default=1)
    cover = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    cover_thumbnail = ImageSpecField(source='cover',
                                     processors=[ResizeToFit(300, 450)],
                                     format='JPEG',
                                     options={'quality': 90})

    @property
    def has_cover(self):
        return bool(self.cover)

    @property
    def cover_thumbnail_url(self):
        return self.cover_thumbnail.url if self.has_cover else None

    def __str__(self):
        return self.title

    def debug_info(self):
        return f"Book(id={self.id}, title='{self.title}', has_cover={self.has_cover}, cover_url='{self.cover.url if self.cover else 'No cover'}')"

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    membership_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Loan(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    loan_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} - {self.member.user.username}"