from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from library.models import Library


class BaseManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get_query_set().get(**kwargs)
        except:
            return None


class BookInfo(models.Model):
    objects = BaseManager()

    title = models.TextField(null=False, blank=False)
    author = models.TextField(null=True, blank=True)
    isbn = models.CharField(max_length=13, null=True, blank=True)
    image_path = models.CharField(max_length=100, null=True, blank=True)

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

    # need to modify... not auto, apply selected date
    created_date = models.DateTimeField(auto_now=True)
    lent_date = models.DateField(null=False)
    return_date = models.DateField(null=False)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return '%s : %s - %s (%s)' % (self.book.book_info.title, str(self.lent_date), str(self.return_date), self.status)
