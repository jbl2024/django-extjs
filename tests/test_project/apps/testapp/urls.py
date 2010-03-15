from django.conf.urls.defaults import *

from extjs.views import query_to_grid
from test_project.apps.testapp.models import Author, Whatamess
from test_project.apps.testapp.models import AuthorGrid, WhatamessGrid

urlpatterns = patterns('',
    url(r'^author/getjson$', query_to_grid,
        kwargs={'modelgrid': AuthorGrid, 'queryset': Author.objects.all()}),
    #url(r'^whatamess/getjson$', query_to_grid,
    #    kwargs={'modelgrid': WhatamessGrid, 'queryset': Whatamess.objects.all()}),
)


