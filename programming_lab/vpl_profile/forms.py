from django import forms
from django.contrib.auth.models import User
from registration.forms import RegistrationForm

class VPLRegistrationForm(RegistrationForm):
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    preferred_name = forms.CharField(max_length=128, required=False)

    def save(self):
        super(VPLRegistrationForm, self).save(commit=False)

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError("This email address is already in use. Please supply a different email address.")
        return self.cleaned_data['email']
