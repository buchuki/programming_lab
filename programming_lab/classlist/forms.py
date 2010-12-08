from django import forms

from classlist.models import ClassList

class RequestClassForm(forms.Form):
    classlist = forms.ModelChoiceField(label="Class",
            queryset=ClassList.objects.all(), empty_label=None,
            widget=forms.RadioSelect)
