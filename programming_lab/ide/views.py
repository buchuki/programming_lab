from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import AuthenticationForm
from vpl_profile.forms import VPLRegistrationForm

@login_required
def main_ide(request):
    return render_to_response("ide/main_ide.html", RequestContext(request, {}))

def index(request):
    registration_form = VPLRegistrationForm()
    authentication_form = AuthenticationForm()
    return render_to_response("index.html", RequestContext(request, 
        {"registration_form": registration_form,
            "authentication_form": authentication_form}))

def about(request):
    return render_to_response("about.html", RequestContext(request, {}))

def contact(request):
    return render_to_response("contact.html", RequestContext(request, {}))
