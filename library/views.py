# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from book.models import *


def library_view(request, library_identifier):

    if library_identifier is None:
        # return library main page
        return HttpResponseRedirect("/")

    library = None
    try:
        if library_identifier.encode('utf8').isdigit():
            library = Library.objects.get(id=library_identifier.encode('utf8'))
        else:
            library = Library.objects.get(name=library_identifier)

        book_list = Book.objects.filter(library__id=library.id).order_by('-id')

    except:
        return HttpResponseRedirect('/')

    return render(
        request,
        'library.djhtml', {
            'library': library,
            'books': book_list,
        }
    )


def library_add(request):

    if request.user.is_authenticated():
        return render(
            request,
            'library_add.djhtml',
            {
            }
        )
    else:
        return HttpResponseRedirect('/')

@csrf_exempt
def library_add_ok(request):

    if request.user.is_authenticated() and request.method == 'POST':

        name = request.POST['name']
        intro = request.POST['intro']

        if name == '':
            return HttpResponse(u'도서관 이름을 입력해 주세요!')

        try:
            Library.objects.get(name=name)

            return HttpResponse(u'중복되는 도서관 이름입니다!')
        except ObjectDoesNotExist:

            library = Library(user=request.user, name=name, intro=intro)
            library.save()

        return HttpResponseRedirect('/library/%s' % library.id)

    return HttpResponseRedirect('/')
