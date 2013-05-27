from haystack import indexes, site

from .models import Book, BookInfo

class BookInfoIndex(indexes.SearchIndex):
    name = indexes.CharField(model_attr='title', document=True)
    author = indexes.CharField(model_attr='author')

    def index_queryset(self):
        return BookInfo.objects.all()

site.register(BookInfo, BookInfoIndex)
"""
class BookIndex(indexes.SearchIndex):
    name = indexes.CharField(model_attr='book_info__title', document=True)
    author = indexes.CharField(model_attr='book_info__author')

    def index_queryset(self):
        return Book.objects.all()

site.register(Book, BookIndex)
"""