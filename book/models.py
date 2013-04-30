from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from library.models import Library

class Book(models.Model):
    library = models.ForeignKey(Library)

    title = models.TextField(null = False, blank = False)
    author = models.TextField(null = True, blank = True)
    isbn = models.CharField(max_length = 13, null = True, blank = True)

    # if data is empty, get data from naver api and save
    # else, return data

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('book', args=[self.id])

    def __unicode__(self):
        return self.title

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

    status = models.CharField(max_length = 2, choices = LEND_STATUS, default = LENT)

    lent_date = models.DateField(auto_now = True, null = False)
    return_date = models.DateField(null = True)

    class Meta:
        ordering = ['-id']

    def __unicode__(self):
        return '%s : %s - %s (%s)' % (self.book.title, str(self.lent_date), str(self.return_date), self.status)