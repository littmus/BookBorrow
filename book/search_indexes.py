from haystack import indexes, site

from .models import Book


class BookIndex(indexes.SearchIndex):
    name = indexes.CharField(model_attr='book_info__title', document=True)
    author = indexes.CharField(model_attr='book_info__author')

    def index_queryset(self):
        return Book.objects.all()

site.register(Book, BookIndex)
