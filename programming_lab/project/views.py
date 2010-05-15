from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from project.models import Project

@login_required
def projects_for_class(request, class_id):
    '''Return a list of classes the logged in user is registered in. Meant to be loaded
    via ajax.'''
    projects = request.user.project_set.filter(classlist__id=class_id)
    return render_to_response('projects/project_list.html',
            RequestContext(request, {'projects': projects}))

@login_required
def create_project(request, class_id):
    '''dum'''
    pass
