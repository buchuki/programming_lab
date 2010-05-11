from django.db import models
from django.contrib.auth.models import User

from classlist.models import ClassList

class Project(models.Model):
    owner = models.ForeignKey(User)
    classlist = models.ForeignKey(ClassList)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)

class File(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=64)
    contents = models.TextField()
