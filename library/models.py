from django.db import models
from django.contrib.auth.models import User

class Library(models.Model):
    user = models.ForeignKey(User)

    name = models.CharField(max_length=100, null=True, blank=True)
    intro = models.TextField(null=True, blank=True)

    #location = models.

    created_at = models.DateTimeField(auto_now=True, null=False)

    #stars = models.IntegerField(null = False, default=0)

    def __unicode__(self):
        return self.name

class Star(models.Model):
    library = models.ForeignKey(Library)
    user = models.ForeignKey(User)
