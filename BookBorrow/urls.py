from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
"""
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
"""
urlpatterns = patterns(
    '',
    url(r'^$', 'BookBorrow.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('account.urls')),
    url(r'^library/', include('library.urls')),
    url(r'^book/', include('book.urls')),
    url(r'^review/', include('review.urls')),
    url(r'^search/', include('haystack.urls')),
   # url(r'^api/', include(android_api.urls)),
    url(r'^whatis/', TemplateView.as_view(template_name='whatis.djhtml')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
