from haystack import indexes

from .models import Book


class BookIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(model_attr='book_info__title', document=True)
    author = indexes.CharField(model_attr='book_info__author')
    
    def get_model(self):
        return Book

    def index_queryset(self, using=None):
        return Book.objects.all()
