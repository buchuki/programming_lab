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
from project.models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = "name", "owner", "classlist", "lab", "project_type"
    list_filter = "owner", "classlist", "lab"
    search_fields = ["name", "classlist__class_name", "lab__name", "owner__username"]

    def queryset(self, request):
        all_projects = super(ProjectAdmin, self).queryset(request)
        if request.user.is_superuser:
            return all_projects
        return all_projects.filter(
                classlist__instructor=request.user) | all_projects.filter(
                        classlist__classtutor__tutor=request.user)

admin.site.register(Project, ProjectAdmin)
