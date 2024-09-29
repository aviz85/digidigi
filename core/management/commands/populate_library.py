from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Author, Book, Member, Loan
from faker import Faker
import random
from datetime import timedelta

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with fake library data'

    def add_arguments(self, parser):
        parser.add_argument('--authors', type=int, default=10, help='Number of authors to create')
        parser.add_argument('--books', type=int, default=50, help='Number of books to create')
        parser.add_argument('--members', type=int, default=20, help='Number of members to create')
        parser.add_argument('--loans', type=int, default=30, help='Number of loans to create')

    def handle(self, *args, **options):
        self.create_authors(options['authors'])
        self.create_books(options['books'])
        self.create_members(options['members'])
        self.create_loans(options['loans'])

        self.stdout.write(self.style.SUCCESS('Successfully populated the library database'))

    def create_authors(self, count):
        for _ in range(count):
            Author.objects.create(
                name=fake.name(),
                birth_date=fake.date_of_birth(minimum_age=20, maximum_age=100),
                biography=fake.paragraph(nb_sentences=3)
            )

    def create_books(self, count):
        authors = list(Author.objects.all())
        for _ in range(count):
            Book.objects.create(
                title=fake.catch_phrase(),
                author=random.choice(authors),
                isbn=fake.isbn13(),
                publication_date=fake.date_between(start_date='-50y', end_date='today'),
                genre=fake.word(),
                description=fake.text(max_nb_chars=200),
                available_copies=random.randint(1, 10)
            )

    def create_members(self, count):
        for _ in range(count):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123'
            )
            Member.objects.create(
                user=user,
                address=fake.address(),
                phone_number=fake.phone_number(),
            )

    def create_loans(self, count):
        books = list(Book.objects.all())
        members = list(Member.objects.all())
        for _ in range(count):
            book = random.choice(books)
            member = random.choice(members)
            loan_date = fake.date_between(start_date='-1y', end_date='today')
            is_returned = random.choice([True, False])
            return_date = fake.date_between(start_date=loan_date, end_date='+30d') if is_returned else None
            
            Loan.objects.create(
                book=book,
                member=member,
                loan_date=loan_date,
                return_date=return_date,
                is_returned=is_returned
            )