from django import forms

from classlist.models import ClassList, ClassRequest

class RequestClassForm(forms.Form):
    classlist = forms.ModelChoiceField(label="Class",
            queryset=ClassList.objects.all(), empty_label=None,
            widget=forms.RadioSelect)

class ApproveRequestForm(forms.Form):
    requests = forms.ModelMultipleChoiceField(
            queryset = ClassRequest.objects.all(),
            widget=forms.CheckboxSelectMultiple)

    def __init__(self, queryset, *args, **kwargs):
        super(ApproveRequestForm, self).__init__(*args, **kwargs)
        self.fields['requests'].queryset = queryset
