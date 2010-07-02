import os 

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from classlist.models import ClassList

class Project(models.Model):
    owner = models.ForeignKey(User)
    classlist = models.ForeignKey(ClassList)
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name

    def is_compilable(self):
        extensions = [f.extension for f in self.file_set.all()]
        if 'java' in extensions:
            return True
        return False

    def file_path(self, filename=None):
        path = os.path.join(settings.STUDENT_PROJECT_FILES, str(self.id))
        if filename:
            path = os.path.join(path, filename)
        return path

class SharedFiles(models.Model):
    project = models.ForeignKey(Project)
    filename = models.CharField(max_length=128)
    shared_with = models.ForeignKey(User)
    shared_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together=("project", "filename", "shared_with")

def extension(filename):
    return filename.rsplit('.')[-1]
