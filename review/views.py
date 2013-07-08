from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Review
from book.models import Book


@login_required
@csrf_exempt
def review_write_ok(request):

    if request.user.is_authenticated() and request.method == 'POST':
        if ('book_info_id' and 'rating' and 'body') in request.POST:
            book_id = request.POST['book_id']
            rating = int(request.POST['rating'])
            body = request.POST['body']

            book = Book.objects.get_or_none(id=book_id)
            if book is None:
                return HttpResponse("-1")

            try:
                review = Review(book=book, user=request.user, rating=rating, body=body)
                review.save()
            except:
                return HttpResponse("-1")

            return HttpResponse("0")

    return HttpResponse("-1")
