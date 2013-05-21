from django.shortcuts import render

from library.models import Library
from book.models import Book


def index(request):

    recently_added_libraries = Library.objects.all()[:5]

    recently_added_books = Book.objects.all()[:5]

    user_library = Library.objects.get_or_none(user__id=request.user.id)

    return render(
        request,
        'index.djhtml',
        {
            'libraries': recently_added_libraries,
            'books': recently_added_books,
            'user_library': user_library,
            #'pop_books': 
        }
    )
