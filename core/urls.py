from django.urls import path
from .views import BookListView, BookDetailView

app_name = 'core'  # This sets the app namespace

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
]