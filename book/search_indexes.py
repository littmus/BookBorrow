from haystack import indexes, site

from .models import Book

class BookIndex(indexes.SearchIndex):
    title = indexes.CharField(model_attr = 'title', document = True)

    def index_queryset(self):
        return Book.objects.all()

site.register(Book, BookIndex)