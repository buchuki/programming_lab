from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from registration.forms import RegistrationForm

@login_required
def main_ide(request):
    return render_to_response("ide/main_ide.html", RequestContext(request, {}))

def index(request):
    registration_form = RegistrationForm()
    return render_to_response("index.html", RequestContext(request, 
        {"registration_form": registration_form}))

def about(request):
    return render_to_response("about.html", RequestContext(request, {}))

def contact(request):
    return render_to_response("contact.html", RequestContext(request, {}))
