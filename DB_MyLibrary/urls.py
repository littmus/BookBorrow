from django.conf.urls import patterns, include, url
from django.contrib import admin

from tastypie.api import Api

from .api import *

admin.autodiscover()

android_api = Api(api_name='android')
android_api.register(UserResource())
android_api.register(LibraryResource())
android_api.register(StarResource())
android_api.register(BookResource())
android_api.register(LendResource())
android_api.register(ReviewResource())

urlpatterns = patterns(
    '',
    url(r'^$', 'DB_MyLibrary.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('account.urls')),
    url(r'^library/', include('library.urls')),
    url(r'^book/', include('book.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'^api/', include(android_api.urls)),
)
