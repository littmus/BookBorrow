from django.contrib.auth.models import User

from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import BasicAuthentication

from library.models import *
from book.models import *
from review.models import * 


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
#        authentication = BasicAuthentication()
        fields = ['id', 'last_name', 'username']


class LibraryResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Library.objects.all()
#        authentication = BasicAuthentication()
#        authorization = DjangoAuthorization()


class StarResource(ModelResource):
    class Meta:
        queryset = Star.objects.all()
#        authentication = BasicAuthentication()
#        authorization = DjangoAuthorization()


class BookResource(ModelResource):
    class Meta:
        queryset = Book.objects.all()
#        authentication = BasicAuthentication()
#        authorization = DjangoAuthorization()


class LendResource(ModelResource):
    class Meta:
        queryset = Lend.objects.all()
#        authentication = BasicAuthentication()
#        authorization = DjangoAuthorization()


class ReviewResource(ModelResource):
    class Meta:
        queryset = Review.objects.all()
#        authentication = BasicAuthentication()
#        authorization = DjangoAuthorization()
