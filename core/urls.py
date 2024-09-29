from django.urls import path
from .views import BookListView

app_name = 'core'  # This sets the app namespace

urlpatterns = [
    path('books/', BookListView.as_view(), name='book_list'),
]