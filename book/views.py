from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from .models import *

#def book_search(isbn):
#    url = 'http://openapi.naver.com/search'
#    key = '5e10771adacbaf7e41fd489ad0cfbf3c'
#    target = 'book_adv'
#    search_query = url + '?key=' + key + '&target=' + target +  

def book_view(request, book_id):

    try:
        book = Book.objects.get(id = book_id)
    except:
        return HttpResponseRedirect('/')

    return render(request, 'book.djhtml', {
            'book': book,
        }
    )