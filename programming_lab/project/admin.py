from django.contrib import admin
from project.models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = "name", "owner", "classlist", "lab", "project_type"
    list_filter = "owner", "classlist", "lab"

admin.site.register(Project, ProjectAdmin)
