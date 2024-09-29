from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Book
from django.core.paginator import Paginator

# Create your views here.

class BookListView(ListView):
    model = Book
    template_name = 'core/book_list.html'
    context_object_name = 'books'
    paginate_by = 12  # Number of books per page

    def get_queryset(self):
        return Book.objects.all().order_by('title')

class BookDetailView(DetailView):
    model = Book
    template_name = 'core/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        print(book.debug_info())
        return context
