from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from book.models import Book


class Review(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)

    body = models.TextField(blank=True)

    # rating : 0 ~ MAX_RATING
    MAX_RATING = 5
    RATING_CHOICES = zip(range(0, MAX_RATING + 1), range(0, MAX_RATING + 1))
    rating = models.PositiveIntegerField(choices=RATING_CHOICES, default=0)

    def get_absolute_url(self):
        return reverse('book', args=[self.book.id])
