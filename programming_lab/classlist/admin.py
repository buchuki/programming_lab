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
from classlist.models import ClassList, ClassTutor

class ClassTutorInline(admin.TabularInline):
    model = ClassTutor

class ClassListAdmin(admin.ModelAdmin):
    filter_horizontal = ['participants']
    inlines = [ClassTutorInline]

    def queryset(self, request):
        all_classes = super(ClassListAdmin, self).queryset(request)
        if request.user.is_superuser:
            return all_classes
        return all_classes.filter(instructor=request.user)

    def log_addition(self, request, object):
        super(ClassListAdmin, self).log_addition(request, object)
        self.update_participants(object)

    def log_change(self, request, object, message):
        super(ClassListAdmin, self).log_change(request, object, message)
        # The add and change views happen to call log_addition and
        # log_change after the object has been saved. I update the
        # m2m at this point (in update_participants) because the add
        # and change views call form.save_m2m() which wipes out the
        # changes if I put it in self.save_model().
        self.update_participants(object)

    def update_participants(self, obj):
        '''Update participants list to ensure instructor and tutors
        are always in it.'''
        if obj.instructor:
            obj.participants.add(obj.instructor)
        for tutor in obj.classtutor_set.all():
            obj.participants.add(tutor.tutor)

class ClassTutorAdmin(admin.ModelAdmin):
    list_filter = ['tutor', 'classlist']
    list_display = ['classlist', 'tutor']
    list_display_links = ['classlist', 'tutor']

    def queryset(self, request):
        all_tutors = super(ClassTutorAdmin, self).queryset(request)
        if request.user.is_superuser:
            return all_tutors
        return all_tutors.filter(classlist__instructor=request.user)

admin.site.register(ClassList, ClassListAdmin)
admin.site.register(ClassTutor, ClassTutorAdmin)
