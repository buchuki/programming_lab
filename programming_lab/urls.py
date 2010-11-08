from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^programming_lab/', include('programming_lab.foo.urls')),

    url(r'^accounts/register/$',
        'registration.views.register',
        {'backend': 'vpl_profile.registration_backend.Registration',
            'success_url': '/ide/'},
        name='registration_register'),
    (r'^accounts/', include('registration.auth_urls')),

    (r'^classlist/', include('classlist.urls')),
    (r'^lab/', include('lab.urls')),
    (r'^projects/', include('project.urls')),
    (r'^chat/', include('chat.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'', include('ide.urls')),
)

if settings.DEBUG == True:
    urlpatterns += patterns('',
        (r'^static/(.*)$', 'django.views.static.serve',{'document_root': settings.PROJECT_HOME + '/static'}),
        (r'^500/$', 'django.views.generic.simple.direct_to_template', {'template': '500.html'}),
        (r'^404/$', 'django.views.generic.simple.direct_to_template', {'template': '404.html'}),
        )
