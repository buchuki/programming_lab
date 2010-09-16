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
