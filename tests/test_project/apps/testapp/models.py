from django.db import models
from django.utils.translation import ugettext_lazy as _

class Author(models.Model):
    TITLE_CHOICES = (
            ('MR', _('Mr.')),
            ('MRS', _('Mrs.')),
            ('MS', _('Ms.')),
    )
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.name

