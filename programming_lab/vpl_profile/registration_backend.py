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

from registration.backends.simple import SimpleBackend
from vpl_profile.forms import VPLRegistrationForm
from vpl_profile.models import UserProfile

class Registration(SimpleBackend):
    def register(self, request, **kwargs):
        new_user = super(Registration,self).register(request, **kwargs)
        new_user.first_name = kwargs['first_name']
        new_user.last_name = kwargs['last_name']
        new_user.save()
        up, created = UserProfile.objects.get_or_create(user=new_user)
        up.preferred_name=kwargs["preferred_name"]
        up.save()
        return new_user

    def get_form_class(self, request):
        return VPLRegistrationForm
