import hashlib
from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape

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

@register.simple_tag
def gravatar(email, size=32):
    digest = hashlib.new('md5', email.lower()).hexdigest()
    url = 'http://www.gravatar.com/avatar/%s?s=%s&d=identicon' % (digest, size)
    return """<img src="%s" height="%s" width="%s"/>""" % (escape(url), size, size)
