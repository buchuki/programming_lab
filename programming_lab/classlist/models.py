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

def setup_staff_signal(sender, instance, created, **kwargs):
    for user in User.objects.all():
        should_be_staff = bool(user.instructed_classes.count()) or bool(user.classtutor_set.all().count())
        if user.is_staff != should_be_staff:
            user.is_staff = should_be_staff
            user.save()

models.signals.post_save.connect(setup_staff_signal, sender=ClassList)
models.signals.post_save.connect(setup_staff_signal, sender=ClassTutor)
