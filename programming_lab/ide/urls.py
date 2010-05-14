from django.conf.urls.defaults import *

urlpatterns = patterns('ide.views',
        url(r'^$', 'main_ide', name='main_ide'),
)
