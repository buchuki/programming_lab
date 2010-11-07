from django.views.decorators.cache import cache_control
import subprocess
import json
import os.path
from zipfile import ZipFile
from cStringIO import StringIO

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse

from project.models import Project, SharedFiles, syntax, editable
from classlist.models import ClassList
from lab.models import Lab
from project.forms import (ProjectForm, NewProjectForm, NewFileForm,
        UploadFileForm) 

@login_required
def projects_for_class(request, class_id):
    '''Return a list of projects the logged in user has associated with that
    class. Meant to be loaded via ajax.'''
    classlist = get_object_or_404(request.user.classes, id=class_id)
    projects = request.user.project_set.filter(classlist=classlist)
    return render_to_response('projects/project_list.html',
            RequestContext(request, {'projects': projects,
                'create_url': reverse('create_class_project', kwargs={'class_id': classlist.id})}))

@login_required
def projects_for_lab(request, lab_id):
    '''Return a list of projects the logged in user has associated with that
    lab. Meant to be loaded via ajax.'''
    lab = get_object_or_404(Lab, id=lab_id)
    projects = request.user.project_set.filter(lab=lab)
    if not projects:
        project = request.user.project_set.create(
                lab=lab,
                name="Default",
                project_type=lab.project_type
                )
        os.makedirs(project.file_path())
        projects = request.user.project_set.filter(lab=lab)
    return render_to_response('projects/project_list.html',
        RequestContext(request, {'projects': projects,
            'create_url': reverse('create_lab_project', kwargs={'lab_id': lab.id})}))

@login_required
def files_for_project(request, project_id):
    '''Return a list of files associated with the given project. Meant to be
    loaded via ajax.'''
    project = get_object_or_404(request.user.project_set, id=project_id)
    files = os.listdir(project.file_path())
    return render_to_response('projects/file_list.html',
            RequestContext(request, {'project': project, 'files': files}))

@login_required
def menu_for_project(request, project_id):
    '''Return a list of menu operations  associated with the given project.
    Meant to be loaded via ajax.'''
    project = get_object_or_404(request.user.project_set, id=project_id)
    return render_to_response('projects/project_menu.html',
            RequestContext(request, {'project': project}))

@login_required
def file_menu(request, project_id, filename):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if not os.path.exists(project.file_path(filename)):
        raise Http404
    return render_to_response('projects/file_menu.html',
            RequestContext(request, {'project': project, 'file': filename}))


def save_new_project(project, user, form):
    project.owner = user
    project.save()
    os.makedirs(project.file_path())
    if form.cleaned_data['initial_filename']:
        path = project.file_path(form.cleaned_data['initial_filename'])
        open(path, 'w').close()
        extra_url = "&filename=%s" % form.cleaned_data['initial_filename']
    else:
        extra_url = ""
    return redirect(project.ide_url() + extra_url)

@login_required
def create_class_project(request, class_id):
    '''Show a form to create a new project attached to a given class.'''
    classlist = get_object_or_404(request.user.classes, id=class_id)

    form = NewProjectForm(request.POST or None)
    if form.is_valid():
        project = form.save(commit=False)
        project.classlist = classlist
        return save_new_project(project, request.user, form)

    return render_to_response("projects/project_form.html",
            RequestContext(request, {'form': form, 'parent': classlist}))

@login_required
def create_lab_project(request, lab_id):
    lab = get_object_or_404(Lab, id=lab_id)

    form = NewProjectForm(request.POST or None,
            initial={'project_type': lab.project_type})
    if form.is_valid():
        project = form.save(commit=False)
        project.lab = lab
        return save_new_project(project, request.user, form)

    return render_to_response("projects/project_form.html",
            RequestContext(request, {'form': form, 'parent': lab}))

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect(project.ide_url())

    return render_to_response("projects/edit_project_form.html",
            RequestContext(request, {'form': form}))

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)

    redirect_url = project.ide_url()

    if request.POST:
        project.delete()
        return redirect(redirect_url)


    return render_to_response("projects/confirm_delete_project.html",
            RequestContext(request, {'project': project, "cancel_url": redirect_url}))

@login_required
def create_file(request, project_id):
    '''Show a form to create a new file attached to a given project.'''
    project = get_object_or_404(request.user.project_set, id=project_id)

    form = NewFileForm(project, request.POST or None)
    if form.is_valid():
        open(form.cleaned_data['name'], 'w').close()

        return redirect(project.ide_url() + "&filename=%s" % (
            os.path.basename(form.cleaned_data['name'])
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

        link = "classlist" if project.classlist else "lab"
        return redirect("/ide/?%s=%s&projectlist=%s&filename=%s" % (
            link,
            project.classlist.id if project.classlist else project.lab.id,
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

@cache_control(no_cache=True, must_revalidate=True)
@login_required
def load_file(request, project_id, filename):
    project = get_object_or_404(Project, id=project_id, owner=request.user)

    if not os.path.exists(project.file_path(filename)):
        raise Http404

    if request.POST:
        if editable(filename):
            with open(project.file_path(filename), 'w') as file:
                file.write(request.POST['contents'])
        return HttpResponse("success")
    else:
        with open(project.file_path(filename)) as file:
            contents = file.read()
        try:
            json.dumps(contents)
        except UnicodeDecodeError:
            contents = "This is a binary file. It cannot be edited.\nUse the File menu above to manipulate it."

        response = {
                'id': '%d/%s' % (project.id, os.path.basename(filename)),
                'title':  os.path.basename(filename),
                'text':   contents,
                'syntax': syntax(filename),
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
            return render_to_response("projects/view_shared_file.html",
                    RequestContext(request, {"filename": filename,
                        "contents": contents, "project": project,
                        "syntax": syntax(filename)}))

@login_required
def view_file(request, project_type, name, projectname, filename):
    if project_type == "class":
        project = get_object_or_404(Project,
                owner=request.user, name=projectname,
                classlist__class_name=name)
    else:
        project = get_object_or_404(Project,
                owner=request.user, name=projectname,
                lab__name=name)
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
def delete_file(request, project_id, filename):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if not os.path.exists(project.file_path(filename)):
        raise Http404

    if project.classlist:
        project_type = "classlist"
        parent_id = project.classlist.id
    else:
        project_type = "lab"
        parent_id = project.lab.id

    redirect_type = "%s=%s" % (project_type, parent_id)
    redirect_url = "/ide/?%s&projectlist=%s&filename=%s" % (redirect_type, project.id, filename)

    if request.POST:
        os.remove(project.file_path(filename))

        return redirect(redirect_url)

    return render_to_response("projects/confirm_delete_file.html",
            RequestContext(request, {'filename': filename, "cancel_url": redirect_url}))

@login_required
def rename_file(request, project_id, filename):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if not os.path.exists(project.file_path(filename)):
        raise Http404

    form = NewFileForm(project, request.POST or None)
    if form.is_valid():
        os.rename(project.file_path(filename), form.cleaned_data['name'])

        return redirect(project.ide_url() + "&filename=%s" % (
            os.path.basename(form.cleaned_data['name'])
            ))

    return render_to_response("projects/file_form.html",
            RequestContext(request, {'form': form, 'project': project,
                'action': "Rename", 'oldname': filename}))

@login_required
def download_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    return render_to_response("projects/download_project.html",
            RequestContext(request, {
                "project": project}))

@login_required
def do_download_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    filename = request.GET.get('filename')
    if not filename:
        filename = project.name
    if not filename.endswith(".zip"):
        filename = filename.zip

    response_string = StringIO()
    archive = ZipFile(response_string, "w")
    for file in os.listdir(project.file_path()):
        archive.write(project.file_path(file), file)
    archive.close()
    response = HttpResponse(response_string.getvalue(), "application/zip")
    response['Content-Disposition'] = "attachment; filename=%s" % (filename)
    return response

compiler_commands = {
    "Web": "javac *.java",
    "Java": "javac *.java",
    "C": "gcc *.c -o '%s'"
}

@login_required
def compile_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    response = None

    command = compiler_commands[project.project_type]
    if "%s" in command:
        command = command % project.name
    output = subprocess.Popen(command, cwd=project.file_path(), shell=True, stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]
    if not output:
        output = "Successful"

    return HttpResponse("<pre>%s\n\n%s</pre>" % (command, output))
