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

class LastRequestMiddleware(object):
    '''Ensure the last request on the user profile has been updated.'''
    def process_request(self, request):
        if request.user.is_authenticated():
            profile = request.user.get_profile()
            profile.last_request = datetime.datetime.now()
            profile.save()
