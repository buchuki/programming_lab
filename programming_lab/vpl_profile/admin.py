from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from vpl_profile.models import UserProfile

admin.site.unregister(User)
class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline]
    search_fields = ('username','email', 'first_name','last_name') 
    list_display = ('username', 'email', 'first_name', 'last_name',
            'is_instructor', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    ordering = ('-last_login',)

    def is_instructor(self, user):
        return bool(user.instructed_classes.count())
    is_instructor.boolean = True
    is_instructor.short_description = "Instructor status"

admin.site.register(User, UserProfileAdmin)
