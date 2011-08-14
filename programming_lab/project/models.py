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

import os.path

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from classlist.models import ClassList
from lab.models import Lab
from project import project_types



class Project(models.Model):
    owner = models.ForeignKey(User)
    classlist = models.ForeignKey(ClassList, null=True, blank=True)
    lab = models.ForeignKey(Lab, null=True, blank=True)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    project_type = models.CharField(max_length=32,
            choices=project_types, default="Other")

    def __unicode__(self):
        return self.name

    def is_compilable(self):
        return self.project_type in ('Java', 'C++')

    def is_viewable(self):
        return "index.html" in os.listdir(self.file_path())

    def file_path(self, filename=None):
        path = os.path.join(settings.STUDENT_PROJECT_FILES, str(self.id))
        if filename:
            path = os.path.join(path, filename)
        return path

    def ide_url(self):
        if self.classlist:
            parent_type = "classlist"
            parent_name = self.classlist.id
        else:
            parent_type = "lab"
            parent_name = self.lab.id
        url = "/ide/?%s=%s&projectlist=%s" % (parent_type, parent_name, self.id)
        return url

    def parent_name(self):
        if self.classlist:
            return self.classlist.class_name
        else:
            return self.lab.name

    def view_url(self):
        if self.classlist:
            parent_type = "class"
            parent_name = self.classlist.class_name
        else:
            parent_type = "lab"
            parent_name = self.lab.name
        url = "/projects/view/%s/%s/%s/" % (parent_type, parent_name, self.name)
        return url

    def source_url(self):
        return self.view_url().replace('view', 'source', 1)


class SharedFiles(models.Model):
    project = models.ForeignKey(Project)
    filename = models.CharField(max_length=128)
    shared_with = models.ForeignKey(User)
    shared_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together=("project", "filename", "shared_with")

def extension(filename):
    if '.' in filename:
        return filename.rsplit('.')[-1].lower()
    return ''

def viewable(filename):
    return editable(filename) or extension(filename) in [
            "png",
            "jpg",
            "gif"
            ]

def editable(filename):
    return extension(filename) in [
            '',
            "html",
            "java",
            "css",
            "js",
            "c",
            "cpp",
            "py"]

syntaxes = {'py': 'python',
        'html': 'htmlmixed',
        'js': 'javascript',
        'java': 'clike',
        'c': 'clike',
        'cpp': 'clike',
        'c++': 'clike'}

def syntax(filename):
    return syntaxes.get(extension(filename), extension(filename))
