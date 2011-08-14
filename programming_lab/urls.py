# This file is part of Virtual Programming Lab.
# 
# Virtual Programming Lab is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Virtual Programming Lab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Virtual Programming Lab.  If not, see <http://www.gnu.org/licenses/>.

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
