import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from classlist.models import ClassList
from project.models import Project, SharedFiles
from chat.models import ChatMessage

@login_required
def logged_in_users(request, class_id):
    '''get the list of logged in users who are associated with the given class.
    A user is defined as logged in if they have made a request in the last
    minute. This should be the case with the ajax poll at the other end.
    
    Efficiency IS an issue here. ;)'''
    users = User.objects.filter(classes__id=class_id).order_by(
            "-userprofile__last_request")
    return render_to_response("chat/user_list.html", RequestContext(request, {
        'users': users}))

@login_required
def chat_messages(request, peer_id):
    peer = get_object_or_404(User, id=peer_id)
    if request.POST:
        message = ChatMessage.objects.create(
                sender=request.user,
                receiver=peer,
                message=request.POST['message'])

    messages = ChatMessage.objects.conversation(request.user, peer)
    messages.filter(receiver=request.user).update(read=True)
    return render_to_response("chat/chat_messages.html", RequestContext(request,
        {"chat_messages": messages}))

@login_required
def share_file(request):
    if request.POST:
        peer = get_object_or_404(User, id=request.POST['share_to'])
        id = request.POST['file_id']
        project_id, filename = id.split('/')
        project = get_object_or_404(Project, owner=request.user, id=project_id)

        shared, created = SharedFiles.objects.get_or_create(
                project=project, filename=filename, shared_with=peer)
        message = ChatMessage.objects.create(
                sender=request.user,
                receiver=peer,
                message_type="send_file",
                message="%s %s " % (filename, project.id))

    messages = ChatMessage.objects.conversation(request.user, peer)
    return render_to_response("chat/chat_messages.html", RequestContext(request,
        {"chat_messages": messages}))
