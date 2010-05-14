from django.db import models
from django.contrib.auth.models import User

class ClassList(models.Model):
    class_name = models.CharField(max_length=128)
    class_number = models.CharField(max_length=8, unique=True)
    participants = models.ManyToManyField(User, related_name="classes", blank=True)

    def __unicode__(self):
        return self.class_name
