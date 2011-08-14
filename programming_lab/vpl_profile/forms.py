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
