from django.db import models
from django.contrib.auth.models import User

class ClassList(models.Model):
    class_name = models.CharField(max_length=128)
    class_number = models.CharField(max_length=8, unique=True)
    participants = models.ManyToManyField(User, related_name="classes", blank=True)
    instructor = models.ForeignKey(User, related_name="instructed_classes",
            blank=True, null=True)

    def __unicode__(self):
        return self.class_name

class ClassTutor(models.Model):
    classlist = models.ForeignKey(ClassList)
    tutor = models.ForeignKey(User)

    def __unicode__(self):
        return self.classlist.class_name + " tutored by " + self.tutor.username
