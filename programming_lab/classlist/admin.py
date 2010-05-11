from django.contrib import admin
from classlist.models import ClassList

class ClassListAdmin(admin.ModelAdmin):
    filter_horizontal = ['participants']


admin.site.register(ClassList, ClassListAdmin)
