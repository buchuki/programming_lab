from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


make_choice = lambda x: ([(p,p) for p in x])

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    last_request = models.DateTimeField(null=True, blank=True)

def user_profile_signal(sender, instance, signal, created, *args, **kwargs):
    '''When a new user is created, ensure a userprofile is associated with it.'''
    if created:
        try:
            user_profile, new = UserProfile.objects.get_or_create(user=instance)
        except Exception, e:
            # Hopefully it is a 'table not found' exception during syncdb
            # and not something important
            print e
            pass

post_save.connect(user_profile_signal, sender=User)
