from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from classlist.models import ClassList
from classlist.forms import RequestClassForm

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
        # process the form
        return redirect("/ide/")

    return render_to_response('classlist/request_class.html',RequestContext(
        request, {
            'form': form
        }))
