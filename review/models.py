from django.db import models
from django.contrib.auth.models import User

from book.models import BookInfo


class Review(models.Model):
    book_info = models.ForeignKey(BookInfo)
    user = models.ForeignKey(User)

    body = models.TextField(blank=True)

    # rating : 0 ~ MAX_RATING
    MAX_RATING = 5
    RATING_CHOICES = zip(range(0, MAX_RATING + 1), range(0, MAX_RATING + 1))
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=0)
