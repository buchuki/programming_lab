from django.db import models
from django.contrib.auth.models import User

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

class File(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=64)
    contents = models.TextField(blank=True)

    @property
    def extension(self):
        return self.name.rsplit('.')[-1]

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ("project", "name")

class SharedFiles(models.Model):
    file = models.ForeignKey(File)
    shared_with = models.ForeignKey(User)
    shared_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together=("file", "shared_with")
