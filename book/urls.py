from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^add/$', 'book.views.book_add'),
    url(r'^add_ok/$', 'book.views.book_add_ok'),
    url(r'^isbn_search/$', 'book.views.book_isbn_search'),
    url(r'^(?P<book_id>\d+)/lend/$', 'book.views.book_lend'),
    url(r'^(?P<book_id>\d+)/lend_req_ok/$', 'book.views.book_lend_req_ok'),
    url(r'^lend/(?P<lend_id>\d+)/lend_process/(?P<lend_action>[\W|\w]+)/$', 'book.views.book_lend_process'),
    url(r'^(?P<book_id>\d+)/$', 'book.views.book_view', name='book'),
)
