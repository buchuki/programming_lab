from django import template
from django.utils.safestring import mark_safe

from chat.models import ChatMessage

register = template.Library()

@register.filter
def chat_status(sender, receiver):
    if ChatMessage.objects.filter(
            sender=sender, receiver=receiver, read=False).count() > 0:
        return "unread"
    elif sender.instructed_classes.all():
        if sender.get_profile().is_online():
            return "online instructor"
        return "instructor"
    elif sender.get_profile().is_online():
        return "online"
    return "offline"
