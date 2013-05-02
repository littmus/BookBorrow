from haystack import indexes, site

from .models import Library

class LibraryIndex(indexes.SearchIndex):
    name = indexes.CharField(model_attr = 'name', document = True)

    def index_queryset(self):
        return Library.objects.all()

site.register(Library, LibraryIndex)
