# This file is part of Virtual Programming Lab.
# 
# Virtual Programming Lab is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Virtual Programming Lab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Virtual Programming Lab.  If not, see <http://www.gnu.org/licenses/>.

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
