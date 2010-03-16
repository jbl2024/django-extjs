from django.db import models
from django.utils.translation import ugettext_lazy as _

class Author(models.Model):
    TITLE_CHOICES = (
            ('MR', _('Mr.')),
            ('MRS', _('Mrs.')),
            ('MS', _('Ms.')),
    )
    name = models.CharField(max_length=100, default="Platon")
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.name

class Whatamess(models.Model):
    TITLE_CHOICES = (
            (1, _('Mr.')),
            (2, _('Mrs.')),
            (3, _('Ms.')),
    )
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    slug = models.SlugField()
    text = models.TextField()
    author = models.ForeignKey(Author)
    title = models.PositiveSmallIntegerField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateTimeField(blank=True, null=True)
    yesno = models.BooleanField()

    def __unicode__(self):
        return self.name

    def yes(self):
        return True

class AuthorProxy(Author):
        class Meta:
            proxy = True

        @property
        def aprint(self):
            return "Proxy here : %s" % self.name

#### GRIDS


from extjs import grids

class AuthorGrid(grids.ModelGrid):
    model = Author
    fields = ['name', 'title', 'birth_date']

class AuthorGridProxy(grids.ModelGrid):
    model = AuthorProxy

class AuthorGrid_nofields(grids.ModelGrid):
    model = Author

class WhatamessGrid(grids.ModelGrid):
    model = Whatamess


