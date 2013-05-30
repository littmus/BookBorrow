from django.contrib.auth.models import User

from tastypie import fields
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS, ALL
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication

from library.models import *
from book.models import *
from review.models import * 


class DefaultModelResource(ModelResource):
    def determine_format(self, request):
        return 'application/json'


class UserResource(DefaultModelResource):
    class Meta:
        queryset = User.objects.all()
#        authentication = BasicAuthentication()
        fields = ['id', 'last_name', 'username']


class LibraryResource(DefaultModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Library.objects.all()
        resource_name = 'library'
#        authentication = BasicAuthentication()
#        authorization = DjangoAuthorization()


class StarResource(DefaultModelResource):
    class Meta:
        queryset = Star.objects.all()
#        authentication = BasicAuthentication()
#        authorization = DjangoAuthorization()


class BookInfoResource(DefaultModelResource):
    class Meta:
        queryset = BookInfo.objects.all()
        excludes = ['isbn']
        resource_name = 'book_info'
        include_resource_uri = False


class BookResource(DefaultModelResource):
    book_info = fields.ForeignKey(BookInfoResource, 'book_info', full=True)

    def build_filters(self, filters=None):
        orm_filters = super(BookResource, self).build_filters(filters)
        if filters and 'library_id' in filters:
            orm_filters['library__id'] = filters['library_id']

        return orm_filters

    class Meta:
        queryset = Book.objects.all()
#        authentication = BasicAuthentication()
#        authorization = DjangoAuthorization()


class LendResource(DefaultModelResource):
    class Meta:
        queryset = Lend.objects.all()
#        authentication = BasicAuthentication()
#        authorization = DjangoAuthorization()


class ReviewResource(DefaultModelResource):
    class Meta:
        queryset = Review.objects.all()
#        authentication = BasicAuthentication()
#        authorization = DjangoAuthorization()
