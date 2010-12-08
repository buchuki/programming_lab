from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from classlist.models import ClassList, ClassRequest
from classlist.forms import RequestClassForm, ApproveRequestForm

@login_required
def classlist(request):
    '''Return a list of classes the logged in user is registered in. Meant to
    be loaded via ajax.'''
    classes = request.user.classes.all()
    return render_to_response('classlist/classlist.html',
            RequestContext(request, {'classes': classes}))

@login_required
def request_class(request):
    form = RequestClassForm(request.POST or None)

    if form.is_valid():
        classlist = form.cleaned_data['classlist']
        if request.user not in classlist.participants.all():
            ClassRequest.objects.create(
                    user=request.user, classlist=classlist)

        return redirect("/ide/")

    return render_to_response('classlist/request_class.html',RequestContext(
        request, {
            'form': form
        }))

@login_required
def approve_requests(request):
    if request.user.is_superuser:
        requests = ClassRequest.objects.filter(status="pending")
    else:
        requests = ClassRequest.objects.filter(status="pending",
                classlist__instructor=request.user)
    form = ApproveRequestForm(requests, request.POST or None)
    
    if form.is_valid():
        form.save()
        return redirect(redirect)
    
    return render_to_response('classlist/approve_request.html',RequestContext(
        request, {
            'form': form
        }))
