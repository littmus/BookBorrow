from django.contrib.auth.models import User

from tastypie import fields
from tastypie.resources import ModelResource, ALL_WITH_RELATIONS
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
        resource_name = 'book_info'


class BookResource(DefaultModelResource):
    book_info = fields.ForeignKey(BookInfoResource, 'book_info', full=True)

    class Meta:
        queryset = Book.objects.select_related()
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
