from django.db import models
from django.contrib.auth.models import User

make_choice = lambda x: ([(p,p) for p in x])

class ChatMessageManager(models.Manager):
    def conversation(self, participant1, participant2):
        return self.filter(sender__in=[participant1, participant2],
                receiver__in=[participant1,participant2])

class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name="sent_chat_messages")
    receiver = models.ForeignKey(User, related_name="received_chat_messages")
    message = models.TextField()
    message_type = models.CharField(max_length=15,
            choices=make_choice(["normal", "send_file"]),
            default="normal")
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    objects = ChatMessageManager()

    def fileinfo(self):
        if self.message_type != "send_file":
            raise ValueError("not a sent message")
        result = dict(zip(("filename", "id"), self.message.split()))
        return result

    class Meta:
        ordering = "timestamp",
