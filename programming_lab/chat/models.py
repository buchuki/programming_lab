from django.db import models
from django.contrib.auth.models import User

class ChatMessageManager(models.Manager):
    def conversation(self, participant1, participant2):
        return self.filter(sender__in=[participant1, participant2],
                receiver__in=[participant1,participant2])

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name="sent_chat_messages")
    receiver = models.ForeignKey(User, related_name="received_chat_messages")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ChatMessageManager()

    class Meta:
        ordering = "timestamp",
