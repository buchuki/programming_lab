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
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from classlist.models import ClassList, ClassRequest
from classlist.forms import RequestClassForm, ApproveRequestForm

@login_required
def classlist(request):
    '''Return a list of classes the logged in user is registered in. Meant to
    be loaded via ajax.'''
    classes = request.user.classes.all()
    return render_to_response('classlist/classlist.html',
            RequestContext(request, {'classes': classes}))

@login_required
def request_class(request):
    form = RequestClassForm(request.POST or None)

    if form.is_valid():
        classlist = form.cleaned_data['classlist']
        if request.user not in classlist.participants.all():
            ClassRequest.objects.create(
                    user=request.user, classlist=classlist)

        return redirect("/ide/")

    return render_to_response('classlist/request_class.html',RequestContext(
        request, {
            'form': form
        }))

@login_required
def approve_requests(request):
    if request.user.is_superuser:
        requests = ClassRequest.objects.filter(status="pending")
    else:
        requests = ClassRequest.objects.filter(status="pending",
                classlist__instructor=request.user)
    form = ApproveRequestForm(requests, request.POST or None)
    
    if form.is_valid():
        approved_requests = form.cleaned_data['requests']
        for r in approved_requests:
            r.status = "approved"
            r.save()
            r.classlist.participants.add(r.user)
        return redirect("/admin/")
    
    return render_to_response('classlist/approve_request.html',RequestContext(
        request, {
            'form': form
        }))
