# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from book.models import *


def HttpAlertResponse(msg):
    return HttpResponse('<script>alert("%s");history.go(-1);</script>' % msg)


@login_required
def library_my(request):
    if request.user.is_authenticated():
        library = Library.objects.get_or_none(user=request.user)

        redirect_url = ''
        if library is not None:
            redirect_url = library.get_absolute_url()
        else:
            redirect_url = '/library/add/'

        return HttpResponseRedirect(redirect_url)
    else:
        return HttpResponseRedirect('/account/login/')


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

        stared = False
        if request.user.is_authenticated():
            star = Star.objects.get_or_none(library=library, user=request.user)
            if star is not None:
                stared = True

    except:
        return HttpResponseRedirect('/')

    return render(
        request,
        'library.djhtml', {
            'library': library,
            'stared': stared,
        }
    )


@login_required
def library_add(request):

    if request.user.is_authenticated():

        library = Library.objects.get_or_none(user=request.user)
        if library is not None:
            return HttpAlertResponse('이미 도서관을 갖고 계세요!')

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
            return HttpAlertResponse('도서관 이름을 입력해 주세요!')

        try:
            Library.objects.get(name=name)

            return HttpAlertResponse(u'중복되는 도서관 이름입니다!')
        except ObjectDoesNotExist:

            library = Library(user=request.user, name=name, intro=intro)
            library.save()

        return HttpResponseRedirect('/library/%s' % library.id)

    return HttpResponseRedirect('/')


@login_required
def library_star(request, library_id):

    if request.user.is_authenticated() and request.method == 'GET':
        try:
            star = Star.objects.get_or_none(library__id=library_id, user=request.user)
            library = Library.objects.get(id=library_id)
            if star is None:
                new_star = Star(library=library, user=request.user)
                new_star.save()
                library.stars += 1
                library.save()
                return HttpResponse('star')
            else:
                star.delete()
                library.stars -= 1
                library.save()
                return HttpResponse('unstar')
        except:
            pass

    return HttpResponse('-1')


def library_star_list(request, library_id):
    library = Library.objects.get_or_none(id=library_id)
    if library is None:
        pass
    stared_users = Star.objects.filter(library=library)
    users = []

    for user in stared_users:
        users.append(user.user)

    return render(
        request,
        'library_star_list.djhtml',
        {
            'library': library,
            'stared_users': users,
        },
    )


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
        lent_books = Lend.objects.filter(book__library__id=library_id, status='LT')

        return render(
            request,
            'library_manage.djhtml',
            {
                'library': library,
                'library_books': library_books,
                'lent_requests': lent_requests,
                'lent_books': lent_books,
            },
        )
    else:
        return HttpResponseRedirect('/')
