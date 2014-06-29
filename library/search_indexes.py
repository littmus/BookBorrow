from haystack import indexes

from .models import Library


class LibraryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(model_attr='name', document=True)
    
    def get_model(self):
        return Library

    def index_queryset(self, using=None):
        return Library.objects.all()
