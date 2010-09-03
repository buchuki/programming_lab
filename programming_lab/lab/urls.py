from django.conf.urls.defaults import *

urlpatterns = patterns('lab.views',
        (r'^$', 'lab_menu'),
)
