from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from classlist.models import ClassList

@login_required
def classlist(request):
    classes = request.user.classes.all()
    return render_to_response("object_list.html",
            RequestContext(request, {
                'objects': classes,
                'title': "List of classes for %s" % request.user,
                }))
