from django.db import models
from django.contrib.auth.models import User

from library.models import Library

class Book(models.Model):
    library = models.ForeignKey(Library)

    title = models.TextField(null=False, blank=False)

    isbn = models.CharField(max_length=13, null=True, blank=True)

    # if data is empty, get data from naver api and save
    # else, return data
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

    def __unicode__(self):
        return "" + str(lent_date) + " - " + str(return_date)