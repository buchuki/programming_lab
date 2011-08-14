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

import datetime
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


make_choice = lambda x: ([(p,p) for p in x])

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    preferred_name = models.CharField(max_length=128, blank=True, default="")
    last_request = models.DateTimeField(null=True, blank=True)

    def is_online(self):
        if self.last_request:
            deadline = datetime.datetime.now() - datetime.timedelta(minutes=1)
            return self.last_request > deadline
        return False

    @property
    def visible_name(self):
        if self.preferred_name:
            return self.preferred_name
        if self.user.get_full_name():
            return self.user.get_full_name()
        return self.user.username

def user_profile_signal(sender, instance, signal, created, *args, **kwargs):
    '''When a new user is created, ensure a userprofile is associated with it.'''
    if created:
        try:
            user_profile, new = UserProfile.objects.get_or_create(user=instance)
        except Exception, e:
            # Hopefully it is a 'table not found' exception during syncdb
            # and not something important
            print e
            pass

post_save.connect(user_profile_signal, sender=User)
