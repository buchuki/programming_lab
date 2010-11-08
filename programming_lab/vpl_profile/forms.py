from django import forms
from registration.forms import RegistrationForm

class VPLRegistrationForm(RegistrationForm):
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    preferred_name = forms.CharField(max_length=128, required=False)

    def save(self):
        super(VPLRegistrationForm, self).save(commit=False)
