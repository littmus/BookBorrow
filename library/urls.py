from django.conf.urls import patterns, url

urlpatterns = patterns('',
                        url(r'^(?P<library_identifier>[\w|\W|\d]+)/$', 'library.views.library_view'),
    )