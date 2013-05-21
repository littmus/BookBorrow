from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^add/$', 'book.views.book_add'),
    url(r'^add_ok/$', 'book.views.book_add_ok'),
    url(r'^isbn_search/$', 'book.views.book_isbn_search'),
    url(r'^(?P<book_id>\d+)/$', 'book.views.book_view', name='book'),
)
