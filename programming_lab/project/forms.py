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
