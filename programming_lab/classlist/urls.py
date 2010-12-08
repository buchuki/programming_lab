from django.conf.urls.defaults import *

urlpatterns = patterns('classlist.views',
        (r'^$', 'classlist'),
        url(r'^request/$', 'request_class', name="request_class_registration"),
)
