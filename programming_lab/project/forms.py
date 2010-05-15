from django import forms
from project.models import Project

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['owner', 'classlist']
