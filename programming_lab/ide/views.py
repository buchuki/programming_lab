from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

@login_required
def main_ide(request):
    return render_to_response("ide/main_ide.html", RequestContext(request, {}))

def index(request):
    return render_to_response("index.html", RequestContext(request, {}))
