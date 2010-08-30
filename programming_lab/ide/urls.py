from django.conf.urls.defaults import *

urlpatterns = patterns('ide.views',
        url(r'^$', 'index', name='index'),
        url(r'^ide/$', 'main_ide', name='main_ide'),
)
