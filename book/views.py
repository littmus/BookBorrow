# -*- coding: utf-8 -*-

import json
import urllib
import urllib2
import xml.etree.ElementTree

from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

import BookBorrow.settings
from .models import *
from library.models import Library


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
                image_url = book_data[2].text
                author = book_data[3].text

                bookinfo = BookInfo(title=title, author=author, isbn=isbn)
                bookinfo.save()

                try:
                    image_name = '%s.jpg' % bookinfo.isbn
                    image_path = BookBorrow.settings.SITE_ROOT + '/..'
                    image_path += BookBorrow.settings.MEDIA_ROOT + BookBorrow.settings.MEDIA_URL
                    image_path += 'images/book/%s' % image_name
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

    try:
        book = Book.objects.get(id=book_id)
    except:
        return HttpResponseNotFound()

    return render(
        request,
        'book.djhtml',
        {
            'book': book,
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
                return HttpResponse('<script>alert("잘못된 ISBN 입니다!");history.go(-1);</script>')

            bookinfo = BookInfo.objects.get(isbn=isbn)

            library = Library.objects.get(user=request.user)
            book = Book(library=library, book_info=bookinfo)
            book.save()

            return HttpResponseRedirect('/library/%s/' % library.id)


    return HttpResponseRedirect('/')


def book_lend(request, book_id):

    try:
        book = Book.objects.get(id=book_id)
    except:
        return HttpResponseNotFound()

    return render(
        request,
        'book_lend.djhtml',
        {
            'book': book,
        }
    )

def book_lend_ok(request, book_id):
    pass
"""
    new_lend = Lent(book=book, user=request.user)
    new_lend.save()
"""

