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
    book = models.ForeignKey(Book)
    user = models.ForeignKey(User)

    LENT = 'LT'
    RETURNED = 'RT'
    OVERDUE = 'OD'
    LEND_STATUS = (
        (LENT, 'lent'),
        (RETURNED, 'returned'),
        (OVERDUE, 'overdue'),
    )

    status = models.CharField(max_length=2, choices=LEND_STATUS, default=LENT)

    # need to modify... not auto, apply selected date
    lent_date = models.DateField(auto_now=True, null=False)
    return_date = models.DateField(null=True)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return '%s : %s - %s (%s)' % (self.book.title, str(self.lent_date), str(self.return_date), self.status)
