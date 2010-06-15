from django.conf.urls.defaults import *

urlpatterns = patterns('project.views',
        (r'^list_for_class/(?P<class_id>\d+)/$', 'projects_for_class'),
        (r'^files_for_project/(?P<project_id>\d+)/$', 'files_for_project'),
        url(r'^download_project/(?P<project_id>\d+)/$', 'download_project',
            name='download_project'),
        url(r'^create/(?P<class_id>\d+)/$', 'create_project', name='create_project'),
        url(r'^create_file/(?P<project_id>\d+)/$', 'create_file', name='create_file'),
        url(r'^upload_new_file/(?P<project_id>\d+)/$', 'upload_new_file', name='upload_new_file'),
        url(r'^file/(?P<file_id>\d+)/$', 'load_file', name='load_file'),
        url(r'^download/(?P<file_id>\d+)/$', 'download_file',
            name='download_file'),
        url(r'^upload/(?P<file_id>\d+)/$', 'upload_replacement_file',
            name='upload_replacement_file'),
        url(r'^view/(?P<classlist>[^/]+)/(?P<projectname>[^/]+)/(?P<filename>[^/]+)$', 'view_file', name='view_file'),
        url(r'^view_shared_file/(?P<file_id>\d+)/$', 'view_shared_file',
            name='view_shared_file'),
)
