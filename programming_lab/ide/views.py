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
from django.contrib.auth.forms import AuthenticationForm
from vpl_profile.forms import VPLRegistrationForm

@login_required
def main_ide(request):
    return render_to_response("ide/main_ide.html", RequestContext(request, {}))

def index(request):
    registration_form = VPLRegistrationForm()
    authentication_form = AuthenticationForm()
    return render_to_response("index.html", RequestContext(request, 
        {"registration_form": registration_form,
            "authentication_form": authentication_form}))

def about(request):
    return render_to_response("about.html", RequestContext(request, {}))

def contact(request):
    return render_to_response("contact.html", RequestContext(request, {}))
