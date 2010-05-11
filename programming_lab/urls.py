from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^programming_lab/', include('programming_lab.foo.urls')),

    url(r'^accounts/register/$',
        'registration.views.register',
        {'backend': 'registration.backends.simple.SimpleBackend',
            'success_url': '/'},
        name='registration_register'),
    (r'accounts/', include('registration.auth_urls')),

    (r'classlist/', include('classlist.urls')),

    (r'^admin/', include(admin.site.urls)),
)
