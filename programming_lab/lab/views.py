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
