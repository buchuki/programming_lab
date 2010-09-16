from django.contrib import admin
from project.models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = "name", "owner", "classlist", "lab", "project_type"
    list_filter = "owner", "classlist", "lab"

    def queryset(self, request):
        all_projects = super(ProjectAdmin, self).queryset(request)
        if request.user.is_superuser:
            return all_projects
        return all_projects.filter(
                classlist__instructor=request.user) | all_projects.filter(
                        classlist__classtutor__tutor=request.user)

admin.site.register(Project, ProjectAdmin)
