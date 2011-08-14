# This file is part of Virtual Programming Lab.
# 
# Virtual Programming Lab is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Virtual Programming Lab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Virtual Programming Lab.  If not, see <http://www.gnu.org/licenses/>.

import datetime
from django.db import models
from django.contrib.auth.models import User

make_choice = lambda x: ([(p,p) for p in x])

class ChatMessageManager(models.Manager):
    def conversation(self, participant1, participant2):
        return self.filter(sender__in=[participant1, participant2],
                receiver__in=[participant1,participant2],
                timestamp__gt=datetime.datetime.now() - datetime.timedelta(
                    seconds=10800)) # 3 hours

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
