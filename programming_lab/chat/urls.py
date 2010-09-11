
from django.conf.urls.defaults import *

urlpatterns = patterns('chat.views',
        (r'^logged_in_to_class/(?P<class_id>\d+)/$', 'logged_in_users'),
        (r'^logged_in_to_lab/(?P<lab_id>\d+)/$', 'logged_in_lab_users'),
        (r'^chat_messages/(?P<peer_id>\d+)/$', 'chat_messages'),
        (r'^share_file/$', 'share_file'),
)
