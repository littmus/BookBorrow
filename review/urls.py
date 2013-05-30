from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^review_write_ok/$', 'review.views.review_write_ok'),
)
