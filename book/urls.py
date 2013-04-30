from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                        url(r'^(?P<book_id>\d+)/$', 'book.views.book_view', name='book'),
)