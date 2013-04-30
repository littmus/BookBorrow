from django.shortcuts import render

from library.models import Library
from book.models import Book

def index(request):

    library_list = Library.objects.all()
    book_list = Book.objects.all()

    return render(request, 'index.djhtml', {
            'libraries': library_list,
            'books': book_list,
        }
    )