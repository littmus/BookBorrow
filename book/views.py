# -*- coding: utf-8 -*-

from datetime import date
import json
import urllib
import urllib2
import xml.etree.ElementTree

from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

import BookBorrow.settings
from .models import *
from library.models import Library
from review.models import Review


def HttpAlertResponse(msg):
    return HttpResponse('<script>alert("%s");history.go(-1);</script>' % msg)

@csrf_exempt
def book_isbn_search(request):

    if request.method == 'POST' and request.user.is_authenticated():
        if 'isbn' in request.POST:
            isbn = request.POST['isbn'].encode('utf-8')

            if len(isbn) != 10 and len(isbn) != 13:
                return HttpResponse('-1')

            bookinfo = BookInfo.objects.get_or_none(isbn=isbn)

            if bookinfo is None:
                key = '141c58846afaf85cd6a5d52e47aa1b86'
                url = 'http://openapi.naver.com/search?key=' + key
                url += '&target=book_adv&query=%s&d_isbn=%s' % (isbn, isbn)

                req = urllib2.Request(url)
                res = urllib2.urlopen(req).read()

                element = xml.etree.ElementTree.XML(res)

                # No search results.
                if (list(element)[0])[4].text == '0':
                    return HttpResponse('-1')
                """
                    0 : title
                    1 : link
                    2 : image link
                    3 : author
                    ...
                """
                book_data = list((list(element)[0])[7])

                title = book_data[0].text
                if title.find(' (') > 0:
                    title = title[:title.find(' (')]
                image_url = book_data[2].text
                author = book_data[3].text

                bookinfo = BookInfo(title=title, author=author, isbn=isbn)
                bookinfo.save()

                try:
                    image_name = '%s.jpg' % bookinfo.isbn
                    #image_path = BookBorrow.settings.SITE_ROOT + '/..'
                    image_path = BookBorrow.settings.MEDIA_ROOT + '/..' + BookBorrow.settings.MEDIA_URL
                    image_path += 'images/book/%s' % image_name
                    print image_path
                    urllib.urlretrieve(image_url[:image_url.find('?')], image_path)
                    bookinfo.image_path = image_name
                    bookinfo.save()

                except Exception as e:
                    print str(e)
                    pass

            bookinfo_data = serializers.serialize('json', [bookinfo, ])
            struct = json.loads(bookinfo_data)
            bookinfo_json = json.dumps(struct[0])

            return HttpResponse(bookinfo_json, mimetype='application/json')
        else:
            return HttpResponse('-1')

    return HttpResponse('-1')


def book_view(request, book_id):

    book = Book.objects.get_or_none(id=book_id)
    if book is None:
        return HttpResponseRedirect('/')

    lend = Lend.objects.get_or_none(book=book, user=request.user, status='RT')
    hasRead = False
    if lend is not None:
        hasRead = True

    reviews = Review.objects.filter(book_info=book.book_info)

    notReviewed = True
    if len(reviews.filter(user=request.user)) != 0:
        notReviewed = False

    canReview = (hasRead or (book.library.user == request.user)) and notReviewed

    return render(
        request,
        'book.djhtml',
        {
            'book': book,
            'canReview': canReview,
            'reviews': reviews,
            'review_avg_rating': book.book_info.get_avg_review_rating,
        }
    )


def book_add(request):

    if request.user.is_authenticated():
        return render(
            request,
            'book_add.djhtml',
        )
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def book_add_ok(request):

    if request.user.is_authenticated() and request.method == 'POST':
        if 'isbn' in request.POST:

            isbn = request.POST['isbn']

            if len(isbn) != 10 and len(isbn) != 13:
                return HttpAlertResponse('잘못된 ISBN 입니다!')

            bookinfo = BookInfo.objects.get(isbn=isbn)

            library = Library.objects.get(user=request.user)
            book = Book(library=library, book_info=bookinfo)
            book.save()

            return HttpResponseRedirect('/library/%s/' % library.id)

    return HttpResponseRedirect('/')


@login_required
def book_delete(request, book_id):

    if request.user.is_authenticated():
        book = Book.objects.get_or_none(id=book_id)
        if book is None:
            pass

        if book.library.user != request:
            pass

        book.delete()

    else:
        pass


@login_required
def book_lend(request, book_id):

    book = Book.objects.get_or_none(id=book_id)
    if book is None:
        return HttpAlertResponse('존재하지 않는 책 입니다!')

    return render(
        request,
        'book_lend.djhtml',
        {
            'book': book,
        }
    )

@csrf_exempt
def book_lend_req_ok(request, book_id):

    if request.method == 'POST' and request.user.is_authenticated():
        if ('start_date' and 'return_date') in request.POST:

            lend_book = Book.objects.get_or_none(id=book_id)

            if lend_book is None:
                return HttpAlertResponse('존재하지 않는 책 입니다!')
            if lend_book.lend_status is True:
                return HttpAlertResponse('대여 중인 책 입니다!')

            s_date = request.POST['start_date'].split('-')
            s_date = map(lambda x: int(x), s_date)
            r_date = request.POST['return_date'].split('-')
            r_date = map(lambda x: int(x), r_date)

            start_date = date(s_date[0], s_date[1], s_date[2])
            return_date = date(r_date[0], r_date[1], r_date[2])

            new_lend = Lend()
            new_lend.book = lend_book
            new_lend.user = request.user
            new_lend.lent_date = start_date
            new_lend.return_date = return_date
            new_lend.save()

            return HttpResponseRedirect(lend_book.get_absolute_url())
    return HttpResponseRedirect('/')


def book_lend_process(request, lend_id, lend_action):
    lend_actions = ['ok', 'reject', 'returned', 'overdue']
    if request.user.is_authenticated():

        lend = Lend.objects.get_or_none(id=lend_id)
        if lend is None:
            return HttpAlertResponse('대여 요청이 존재하지 않습니다!')

        if lend_action not in lend_actions:
            return HttpAlertResponse('잘못된 동작입니다!')

        if lend_action == 'ok':
            lend.status = 'LT'
            lend.book.lend_status = True
            lend.book.save()
        elif lend_action == 'reject':
            lend.status = 'RJ'
        elif lend_action == 'returned':
            lend.status = 'RT'
            lend.book.lend_status = False
            lend.book.save()
        elif lend_action == 'overdue':
            lend.status = 'OD'

        lend.save()

        library_id = Library.objects.get(user=request.user).id

        return HttpResponseRedirect('/library/%s/manage/' % library_id)

    return HttpResponseRedirect('/')
