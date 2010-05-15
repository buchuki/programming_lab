from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from classlist.models import ClassList

@login_required
def classlist(request):
    '''Return a list of classes the logged in user is registered in. Meant to be loaded
    via ajax.'''
    classes = request.user.classes.all()
    return render_to_response('classlist/classlist.html',
            RequestContext(request, {'classes': classes}))
