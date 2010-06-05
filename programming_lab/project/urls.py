from django.conf.urls.defaults import *

urlpatterns = patterns('project.views',
        (r'^list_for_class/(?P<class_id>\d+)/$', 'projects_for_class'),
        (r'^files_for_project/(?P<project_id>\d+)/$', 'files_for_project'),
        url(r'^create/(?P<class_id>\d+)/$', 'create_project', name='create_project'),
        url(r'^create_file/(?P<project_id>\d+)/$', 'create_file', name='create_file'),
        url(r'^file/(?P<file_id>\d+)/$', 'load_file', name='load_file'),
        url(r'^view_shared_file/(?P<file_id>\d+)/$', 'view_shared_file',
            name='view_shared_file'),
)
