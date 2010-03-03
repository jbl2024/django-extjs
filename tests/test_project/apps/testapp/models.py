from django.db import models


class Author(models.Model):
    TITLE_CHOICES = (
            ('MR', 'Mr.'),
            ('MRS', 'Mrs.'),
            ('MS', 'Ms.'),
    )
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.name

