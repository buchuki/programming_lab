import subprocess
import json
import os.path
import tempfile
from zipfile import ZipFile
from cStringIO import StringIO

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.template import RequestContext

from project.models import Project, SharedFiles, extension
from classlist.models import ClassList
from project.forms import NewProjectForm, NewFileForm, UploadFileForm

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
    files = os.listdir(project.file_path())
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

    form = NewFileForm(project, request.POST or None)
    if form.is_valid():
        open(form.cleaned_data['name'], 'w').close()

        return redirect("/?classlist=%s&projectlist=%s&filename=%s" % (
            project.classlist.id,
            project.id,
            form.cleaned_data['name']
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
        with open(project.file_path(file_info.name), 'w') as file:
            for chunk in file_info.chunks():
                file.write(chunk)
        return redirect("/?classlist=%s&projectlist=%s&filename=%s" % (
            project.classlist.id,
            project.id,
            file_info.name
            ))

    return render_to_response("projects/upload_file.html",
            RequestContext(request, {'form': form, 'project': project,
                'is_new': True}))

@login_required
def upload_replacement_file(request, project_id, filename):
    project = get_object_or_404(request.user.project_set, id=project_id)

    form = UploadFileForm(project, False,
            request.POST or None, request.FILES or None)

    if form.is_valid():
        file_info = form.cleaned_data['file']
        with open(project.file_path(filename), 'w') as file:
            for chunk in file_info.chunks():
                file.write(chunk)

        return redirect("/?classlist=%s&projectlist=%s&filename=%s" % (
            project.classlist.id,
            project.id,
            filename
            ))

    return render_to_response("projects/upload_file.html",
            RequestContext(request, {'form': form, 'project': project,
                'is_new': False, "file": filename}))

@login_required
def load_file(request, project_id, filename):
    project = get_object_or_404(Project, id=project_id, owner=request.user)

    if not os.path.exists(project.file_path(filename)):
        raise Http404

    if request.POST:
        with open(project.file_path(filename), 'w') as file:
            file.write(request.POST['contents'])
        return HttpResponse("success")
    else:
        with open(project.file_path(filename)) as file:
            contents = file.read()

        response = {
                'id': '%d/%s' % (project.id, os.path.basename(file.name)),
                'title':  os.path.basename(filename),
                'text':   contents,
                'syntax': extension(filename),
                }
        return HttpResponse(json.dumps(response), mimetype="application/json")

@login_required
def view_shared_file(request, project_id, filename):
    project = get_object_or_404(Project, id=project_id)

    if not os.path.exists(project.file_path(filename)):
        raise Http404

    try:
        shared_file = SharedFiles.objects.get(project=project, filename=filename,
                shared_with=request.user)
    except SharedFiles.DoesNotExist:
        return HttpResponse("The file you requested has not been shared with you.")
    else:
        with open(project.file_path(filename)) as file:
            contents = file.read()
            print contents
            return render_to_response("projects/view_shared_file.html",
                    RequestContext(request, {"filename": filename,
                        "contents": contents, "project": project,
                        "extension": extension(filename)}))

@login_required
def view_file(request, classlist, projectname, filename):
    project = get_object_or_404(Project,
            owner=request.user, name=projectname,
            classlist__class_name=classlist)
    try:
        with open(project.file_path(filename)) as file:
            return HttpResponse(file.read())
    except IOError:
        raise Http404

@login_required
def download_file(request, project_id, filename):
    project = get_object_or_404(Project, id=project_id, owner=request.user)

    if not os.path.exists(project.file_path(filename)):
        raise Http404
    with open(project.file_path(filename)) as file:
        response = HttpResponse(file.read(), "application/octet-stream")
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

@login_required
def compile_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    temp_path = tempfile.mkdtemp("vpl_compile_%s" % project_id)
    response = None
    try:
        for file in project.file_set.filter(name__endswith=".java"):
            filepath = os.path.join(temp_path, file.name)
            with open(filepath, 'w') as openfile:
                openfile.write(file.contents)
                print file.contents

        output = subprocess.Popen('/opt/java/bin/javac *.java', cwd=temp_path, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]
        if not output:
            output = "Successful"
            # way too special casey. Should probably store files on the
            # filesystem to begin with
            for filename in [f for f in os.listdir(temp_path) if f.endswith('.class')]:
                file, created = project.file_set.get_or_create(name=filename)
                filepath = os.path.join(temp_path, file.name)
                print filepath
                with open(filepath) as openfile:
                    file.contents = base64.encodestring(openfile.read())
                file.save()
        return HttpResponse("<pre>javac *.java\n\n%s</pre>" % output)
    finally:
        import shutil
        shutil.rmtree(temp_path)
