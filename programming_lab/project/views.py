from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import RequestContext
from project.models import Project, File
from classlist.models import ClassList
from project.forms import NewProjectForm, NewFileForm

@login_required
def projects_for_class(request, class_id):
    '''Return a list of projects the logged in user has associated with that
    class. Meant to be loaded via ajax.'''
    classlist = get_object_or_404(request.user.classes, id=class_id)
    projects = request.user.project_set.filter(classlist=classlist)
    return render_to_response('projects/project_list.html',
            RequestContext(request, {'projects': projects, 'classlist': classlist}))

@login_required
def files_for_project(request, project_id):
    '''Return a list of files associated with the given project. Meant to be
    loaded via ajax.'''
    project = get_object_or_404(request.user.project_set, id=project_id)
    files = project.file_set.all()
    return render_to_response('projects/file_list.html',
            RequestContext(request, {'project': project, 'files': files}))

@login_required
def create_project(request, class_id):
    '''Show a form to create a new project attached to a given class.'''
    classlist = get_object_or_404(request.user.classes, id=class_id)

    form = NewProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.classlist = classlist
        project.owner = request.user
        project.save()
        return redirect("/")

    return render_to_response("projects/project_form.html",
            RequestContext(request, {'form': form, 'classlist': classlist}))

@login_required
def create_file(request, project_id):
    '''Show a form to create a new file attached to a given project.'''
    project = get_object_or_404(request.user.project_set, id=project_id)

    form = NewFileForm(request.POST or None)
    if form.is_valid():
        file = form.save(commit=False)
        file.project = project
        file.save()
        return redirect("/")

    return render_to_response("projects/file_form.html",
            RequestContext(request, {'form': form, 'project': project}))

@login_required
def load_file(request, file_id):
    file = get_object_or_404(File, id=file_id, project__owner=request.user)
    return HttpResponse(file.contents)
