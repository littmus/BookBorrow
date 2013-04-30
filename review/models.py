from django.db import models
from django.contrib.auth.models import User

from book.models import Book

class Review(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)

    title = models.CharField(max_length = 100, blank = True)
    body = models.TextField(blank = True)

    # rating : 1 ~ 5
    MAX_RATING = 5
    RATING_CHOICES = zip(range(1, MAX_RATING + 1), range(1, MAX_RATING + 1))
    rating = models.PositiveIntegerField(choices = RATING_CHOICES, default = 1)