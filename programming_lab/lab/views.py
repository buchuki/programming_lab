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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from lab.models import Lab

@login_required
def lab_menu(request):
    '''Return a list of classes the logged in user is registered in. Meant to be loaded
    via ajax.'''
    labs = Lab.objects.all()
    return render_to_response('lab/labs.html',
            RequestContext(request, {'labs': labs}))
