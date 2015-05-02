from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from library.models import Library


class BaseManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get_queryset().get(**kwargs)
        except:
            return None


class BookInfo(models.Model):
    objects = BaseManager()

    title = models.TextField(null=False, blank=False)
    author = models.TextField(null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)

    def get_avg_review_rating(self):
        from review.models import Review
        reviews = Review.objects.filter(book__book_info=self)
        ratings = [review.rating for review in reviews]

        review_avg_rating = '0.00'
        if len(ratings) != 0:
            review_avg_rating = '%.2f' % (reduce(lambda x, y: x + y, ratings) / float(len(ratings)))

        return review_avg_rating

    def __unicode__(self):
        return self.title


class Book(models.Model):
    objects = BaseManager()

    library = models.ForeignKey(Library)
    book_info = models.ForeignKey(BookInfo)

    lend_status = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('book', args=[self.id])

    def get_lents_count(self):
        return len(Lend.objects.filter(book__id=self.id, status='RT'))

    def __unicode__(self):
        return self.book_info.title


class Lend(models.Model):
    objects = BaseManager()

    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)

    REQUEST = 'RQ'
    LENT = 'LT'
    REJECTED = 'RJ'
    RETURNED = 'RT'
    OVERDUE = 'OD'
    LEND_STATUS = (
        (REQUEST, 'request'),
        (LENT, 'lent'),
        (REJECTED, 'rejected'),
        (RETURNED, 'returned'),
        (OVERDUE, 'overdue'),
    )

    status = models.CharField(max_length=2, choices=LEND_STATUS, default=REQUEST)

    created_date = models.DateTimeField(auto_now=True)
    lent_date = models.DateField(null=False)
    return_date = models.DateField(null=False)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return '%s : %s - %s (%s)' % (self.book.book_info.title, str(self.lent_date), str(self.return_date), self.status)
