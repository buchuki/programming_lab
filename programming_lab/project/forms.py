from django import forms
from project.models import Project, File

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['owner', 'classlist']

class NewFileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ['project', 'contents']
