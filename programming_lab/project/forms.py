import os.path

from django import forms
from django.conf import settings

from project.models import Project

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['owner', 'classlist']

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
        if self.require_unique:
            try:
                file = self.project.file_set.get(
                        name=self.cleaned_data['file'].name)
            except File.DoesNotExist:
                return self.cleaned_data['file']
            else:
                raise forms.ValidationError("That filename already exists")
        return self.cleaned_data['file']
