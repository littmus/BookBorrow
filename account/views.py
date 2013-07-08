# -*- coding: utf-8 -*-

from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from book.models import Lend
from review.models import Review


def validateEmail(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    try:
        validate_email(email)
        return True

    except ValidationError:
        return False


def join_view(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        return render(request, 'join.djhtml')


def checkEmail(request):

    if request.method == 'POST' and 'email' in request.POST:
        email = request.POST['email']

        if email == '':
            return HttpResponse('Please input email')

        try:
            user = User.objects.get(email=email)
            return HttpResponse('Duplicate email')
        except User.DoesNotExist:
            return HttpResponse('Ok')


class invalidParam(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


@csrf_exempt
def join_ok(request):

    if request.method == 'POST':
        try:
            try:
                id = request.POST['id']
                password = request.POST['password']
                name = request.POST['name']
                email = request.POST['email']

            except:
                raise invalidParam('Missing param')

            if not validateEmail(email):
                raise invalidParam('email')

            if not (0 < len(id) <= 20):
                raise invalidParam('id')

            if not (6 <= len(password) <= 20):
                raise invalidParam('password')

            try:
                User.objects.get(username=id)
                return HttpResponse("<script> alert(\"error1\"); history.go(-1); </script>")
            except User.DoesNotExist:
                pass

            user = User.objects.create_user(username=id, email=email, password=password)

            user.last_name = name
            user.save()

            user = authenticate(username=id, password=password)
            login(request, user)

            return HttpResponseRedirect('/')

        except invalidParam:
            return HttpResponse("<script> alert(\"error2 " + str(invalidParam) + "\"); history.go(-1); </script>")

    else:
        return HttpResponseRedirect('/')


def login_view(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    return_to = ''
    if 'return_to' in request.GET:
        return_to = request.GET['return_to']

    return render(
        request,
        'login.djhtml',
        {
            'return_to': return_to,
        })


@csrf_exempt
def login_ok(request):

    if request.method == "POST" and ('id' and 'password' in request.POST):

        if request.user.is_authenticated():
            return HttpResponseRedirect('/')

        id = request.POST['id']
        password = request.POST['password']

        user = authenticate(username=id, password=password)

        if user is not None:
            if user.is_active:

                login(request, user)

                if 'return_to' in request.GET:
                    return HttpResponseRedirect(request.GET['return_to'])
                else:
                    return HttpResponseRedirect('/')
            else:
                return HttpResponse('<script> alert("잘못된 계정입니다!"); history.go(-1); </script>')
        else:
            return HttpResponse('<script> alert("로그인에 실패했습니다!"); history.go(-1); </script>')
    else:
        HttpResponseRedirect('/')


def logout_ok(request):
    if request.user.is_authenticated():
        logout(request)

    return HttpResponseRedirect('/')


def mypage_view(request):
    if request.user.is_authenticated():
        lent_books = Lend.objects.filter(user=request.user)
        reviews = Review.objects.filter(user=request.user)
        return render(
            request,
            'mypage.djhtml',
            {
                'lent_books': lent_books,
                'reviews': reviews,
            }
        )
    return HttpResponseRedirect('/')
