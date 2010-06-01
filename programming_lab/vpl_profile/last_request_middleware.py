import datetime

class LastRequestMiddleware(object):
    '''Ensure the last request on the user profile has been updated.'''
    def process_request(self, request):
        if request.user.is_authenticated():
            profile = request.user.get_profile()
            profile.last_request = datetime.datetime.now()
            profile.save()
