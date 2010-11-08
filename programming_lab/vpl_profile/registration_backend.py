from registration.backends.simple import SimpleBackend
from vpl_profile.forms import VPLRegistrationForm
from vpl_profile.models import UserProfile

class Registration(SimpleBackend):
    def register(self, request, **kwargs):
        new_user = super(Registration,self).register(request, **kwargs)
        new_user.first_name = kwargs['first_name']
        new_user.last_name = kwargs['last_name']
        new_user.save()
        up, created = UserProfile.objects.get_or_create(user=new_user)
        up.preferred_name=kwargs["preferred_name"]
        up.save()
        return new_user

    def get_form_class(self, request):
        return VPLRegistrationForm
