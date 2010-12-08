from django.db import models
from django.contrib.auth.models import User, Group

make_choice = lambda x: ([(p,p) for p in x])

class ClassList(models.Model):
    class_name = models.CharField(max_length=128)
    class_number = models.CharField(max_length=8, unique=True)
    participants = models.ManyToManyField(User, related_name="classes", blank=True)
    instructor = models.ForeignKey(User, related_name="instructed_classes",
            blank=True, null=True)

    def __unicode__(self):
        return "%s: %s" % (self.class_number, self.class_name)

    class Meta:
        verbose_name="Class"
        verbose_name_plural="Classes"

class ClassTutor(models.Model):
    classlist = models.ForeignKey(ClassList)
    tutor = models.ForeignKey(User)

    def __unicode__(self):
        return self.classlist.class_name + " tutored by " + self.tutor.username

class ClassRequest(models.Model):
    user = models.ForeignKey(User)
    classlist = models.ForeignKey(ClassList)
    status = models.CharField(max_length=16, choices=make_choice(
        ["pending", "rejected", "approved"]),
        default="pending")

def setup_staff_signal(sender, instance, created, **kwargs):
    '''Ensures all users have proper staff status and groups. This is overkill
    and expensive, but this signal should be called relatively infrequently.'''

    for user in User.objects.all():
        is_instructor = bool(user.instructed_classes.count())
        is_tutor = bool(user.classtutor_set.count())
        is_super = user.is_superuser
        should_be_staff = any((is_tutor, is_instructor, is_super))
        if user.is_staff != should_be_staff:
            user.is_staff = should_be_staff
            user.save()

        if is_instructor:
            user.groups.add(Group.objects.get(name="instructors"))
        else:
            user.groups.remove(Group.objects.get(name="instructors"))

        if is_tutor:
            user.groups.add(Group.objects.get(name="tutors"))
        else:
            user.groups.remove(Group.objects.get(name="tutors"))

models.signals.post_save.connect(setup_staff_signal, sender=ClassList)
models.signals.post_save.connect(setup_staff_signal, sender=ClassTutor)
