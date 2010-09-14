from django.conf.urls.defaults import *

urlpatterns = patterns('project.views',
        (r'^list_for_class/(?P<class_id>\d+)/$', 'projects_for_class'),
        (r'^list_for_lab/(?P<lab_id>\d+)/$', 'projects_for_lab'),
        (r'^files_for_project/(?P<project_id>\d+)/$', 'files_for_project'),
        (r'^menu_for_project/(?P<project_id>\d+)/$', 'menu_for_project'),
        url(r'^download_project/(?P<project_id>\d+)/$', 'download_project',
            name='download_project'),
        url(r'^create_class_project/(?P<class_id>\d+)/$', 'create_class_project', name='create_class_project'),
        url(r'^create_lab_project/(?P<lab_id>\d+)/$', 'create_lab_project', name='create_lab_project'),
        url(r'^file_menu/(?P<project_id>\d+)/(?P<filename>[^/]+)/$', 'file_menu'),
        url(r'^create_file/(?P<project_id>\d+)/$', 'create_file', name='create_file'),
        url(r'^upload_new_file/(?P<project_id>\d+)/$', 'upload_new_file', name='upload_new_file'),
        url(r'^file/(?P<project_id>\d+)/(?P<filename>[^/]+)/$', 'load_file', name='load_file'),
        url(r'^download/(?P<project_id>\d+)/(?P<filename>[^/]+)/$', 'download_file',
            name='download_file'),
        url(r'^upload/(?P<project_id>\d+)/(?P<filename>[^/]+)/$', 'upload_replacement_file',
            name='upload_replacement_file'),
        url(r'^(?P<project_id>\d+)/delete_file/(?P<filename>[^/]+)/$', 'delete_file',
            name='delete_file'),
        url(r'^compile/(?P<project_id>\d+)/$', 'compile_project', name='compile_project'),
        url(r'^view/(?P<project_type>class|lab)/(?P<name>[^/]+)/(?P<projectname>[^/]+)/(?P<filename>[^/]+)$', 'view_file', name='view_file'),
        url(r'^view_shared_file/(?P<project_id>\d+)/(?P<filename>[^/]+)/$', 'view_shared_file',
            name='view_shared_file'),
)
