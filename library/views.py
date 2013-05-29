# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
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


def library_star(request, library_id):

    if request.user.is_authenticated() and request.method == 'POST':
        try:
            star = Star.objects.get_or_none(library__id=library_id, user=request.user)
            if star is None:
                library = Library.objects.get(id=library_id)
                new_star = Star(library=library, user=request.user)
            else:
                star.delete()

            return HttpResponse('0')
        except:
            pass

    return HttpResponse('-1')

@login_required
def library_manage(request, library_id):

    if request.user.is_authenticated():
        library = Library.objects.get_or_none(id=library_id)
        if library is None:
            return HttpResponseRedirect('/')

        if library.user != request.user:
            return HttpResponseRedirect('/')

        library_books = Book.objects.filter(library__id=library_id)
        lent_requests = Lend.objects.filter(book__library__id=library_id, status='RQ')

        return render(
            request,
            'library_manage.djhtml',
            {
                'library': library,
                'library_books': library_books,
                'lent_requests': lent_requests,
            },
        )
    else:
        return HttpResponseRedirect('/')
