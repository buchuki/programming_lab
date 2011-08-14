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

urlpatterns = patterns('chat.views',
        (r'^logged_in_to_class/(?P<class_id>\d+)/$', 'logged_in_users'),
        (r'^logged_in_to_lab/(?P<lab_id>\d+)/$', 'logged_in_lab_users'),
        (r'^chat_messages/(?P<peer_id>\d+)/$', 'chat_messages'),
        (r'^share_file/$', 'share_file'),
)
