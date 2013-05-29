from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class BaseManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get_query_set().get(**kwargs)
        except:
            return None


class Library(models.Model):
    objects = BaseManager()

    user = models.ForeignKey(User)

    name = models.CharField(max_length=100, null=True, blank=True)
    intro = models.TextField(null=True, blank=True)
    #location = models.CharField(max_length=100, null=True, blank=True)

    created_at = models.DateTimeField(auto_now=True, null=False)

    stars = models.IntegerField(null=False, default=0)

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse('library', args=[self.id])

    def get_starts_count(self):
        return len(Star.objects.filter(library__id=self.id))

    def __unicode__(self):
        return self.name


class Star(models.Model):
    objects = BaseManager()

    library = models.ForeignKey(Library)
    user = models.ForeignKey(User)

    created_at = models.DateTimeField(auto_now=True, null=False)
