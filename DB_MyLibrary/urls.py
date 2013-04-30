from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                        url(r'^$', 'DB_MyLibrary.views.index'),
                        url(r'^admin/', include(admin.site.urls)),
                        url(r'^account/', include('account.urls')),
                        url(r'^library/', include('library.urls')),
                        url(r'^book/', include('book.urls')),
                        url(r'^search/', include('haystack.urls')),

    # Examples:
    # url(r'^$', 'DB_MyLibrary.views.home', name='home'),
    # url(r'^DB_MyLibrary/', include('DB_MyLibrary.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)