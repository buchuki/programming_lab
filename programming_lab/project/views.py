from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from project.models import Project
from classlist.models import ClassList
from project.forms import NewProjectForm

@login_required
def projects_for_class(request, class_id):
    '''Return a list of classes the logged in user is registered in. Meant to be loaded
    via ajax.'''
    classlist = get_object_or_404(ClassList, id=class_id, participants=request.user)
    projects = request.user.project_set.filter(classlist=classlist)
    return render_to_response('projects/project_list.html',
            RequestContext(request, {'projects': projects, 'classlist': classlist}))

@login_required
def create_project(request, class_id):
    '''Show a form to create a new project attached to a given class.'''
    classlist = get_object_or_404(ClassList, id=class_id, participants=request.user)

    form = NewProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.classlist = classlist
        project.owner = request.user
        project.save()
        return redirect("/")

    return render_to_response("projects/project_form.html",
            RequestContext(request, {'form': form, 'classlist': classlist}))
