from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import RequestContext
from project.models import Project, File, SharedFiles
from classlist.models import ClassList
from project.forms import NewProjectForm, NewFileForm, UploadFileForm
import json
from zipfile import ZipFile
from cStringIO import StringIO

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
        return redirect("/?classlist=%s&projectlist=%s" % (classlist.id, project.id))

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
        return redirect("/?classlist=%s&projectlist=%s&file_id=%s" % (
            project.classlist.id,
            project.id,
            file.id
            ))

    return render_to_response("projects/file_form.html",
            RequestContext(request, {'form': form, 'project': project}))

@login_required
def upload_new_file(request, project_id):
    project = get_object_or_404(request.user.project_set, id=project_id)
    form = UploadFileForm(project, True, 
            request.POST or None, request.FILES or None)
    if form.is_valid():
        file_info = form.cleaned_data['file']
        file = File(project=project, name=file_info.name,
                contents=file_info.read())
        file.save()
        return redirect("/?classlist=%s&projectlist=%s&file_id=%s" % (
            project.classlist.id,
            project.id,
            file.id
            ))

    return render_to_response("projects/upload_file.html",
            RequestContext(request, {'form': form, 'project': project,
                'is_new': True}))

@login_required
def load_file(request, file_id):
    try:
        file = get_object_or_404(File, id=file_id, project__owner=request.user)
        if request.POST:
            file.contents = request.POST['contents']
            file.save()
            return HttpResponse("success")
        else:
            response = {
                    'id': str(file.id),
                    'title': file.name,
                    'text': file.contents,
                    'syntax': file.extension,
                    }
            return HttpResponse(json.dumps(response), mimetype="application/json")
    except Exception as e:
        print e

@login_required
def view_shared_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    try:
        shared_file = SharedFiles.objects.get(file=file, shared_with=request.user)
    except SharedFiles.DoesNotExist:
        return HttpResponse("The file you requested has not been shared with you.")
    else:
        return render_to_response("projects/view_shared_file.html",
                RequestContext(request, {"file": file}))

@login_required
def view_file(request, classlist, projectname, filename):
    file = get_object_or_404(File, name=filename,
            project__owner=request.user, project__name=projectname,
            project__classlist__class_name=classlist)
    return HttpResponse(file.contents)

@login_required
def download_file(request, file_id):
    file = get_object_or_404(File, id=file_id, project__owner=request.user)
    response = HttpResponse(file.contents, "application/octet-stream")
    response['Content-Disposition'] = "attachment; filename=%s" % file.name
    return response

@login_required
def download_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    response_string = StringIO()
    archive = ZipFile(response_string, "w")
    for file in project.file_set.all():
        archive.writestr(file.name, file.contents)
    archive.close()
    response = HttpResponse(response_string.getvalue(), "application/zip")
    response['Content-Disposition'] = "attachment; filename=%s.zip" % project.name
    return response
