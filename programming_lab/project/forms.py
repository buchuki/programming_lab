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

from django import forms
from django.conf import settings

from project.models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['owner', 'classlist', 'lab']

class NewProjectForm(ProjectForm):
    initial_filename = forms.CharField(help_text="Name a file to add to the project",
            required=False)
    class Meta:
        model = Project
        exclude = ['owner', 'classlist', 'lab']

class NewFileForm(forms.Form):
    name = forms.CharField()

    def __init__(self, project, *args, **kwargs):
        self.project = project
        super(NewFileForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        path = self.project.file_path(self.cleaned_data['name'])

        if os.path.exists(path):
            raise forms.ValidationError("That filename already exists")
        return path

class UploadFileForm(forms.Form):
    file = forms.FileField()

    def __init__(self, project, require_unique, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.project = project
        self.require_unique =require_unique

    def clean_file(self):
        path = self.project.file_path(self.cleaned_data['file'].name)
        if self.require_unique and os.path.exists(path):
                raise forms.ValidationError("That filename already exists")

        return self.cleaned_data['file']
