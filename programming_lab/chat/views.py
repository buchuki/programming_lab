import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from classlist.models import ClassList

@login_required
def logged_in_users(request, class_id):
    '''get the list of logged in users who are associated with the given class.
    A user is defined as logged in if they have made a request in the last
    minute. This should be the case with the ajax poll at the other end.
    
    Efficiency IS an issue here. ;)'''
    deadline = datetime.datetime.now() - datetime.timedelta(minutes=1)
    users = User.objects.filter(classes__id=class_id,
            userprofile__last_request__gt=deadline)
    return render_to_response("chat/user_list.html", RequestContext(request, {
        'users': users}))

@login_required
def chat_messages(request, peer_id):
    from django.http import HttpResponse
    return HttpResponse("HAHA")
