from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^programming_lab/', include('programming_lab.foo.urls')),

    (r'^admin/', include(admin.site.urls)),
)
