from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^add/$', 'library.views.library_add'),
    url(r'^add_ok/$', 'library.views.library_add_ok'),
    url(r'^(?P<library_id>\d+)/manage/$', 'library.views.library_manage'),
    url(r'^(?P<library_identifier>[\w|\W|\d]+)/$', 'library.views.library_view'),
)
