from django.contrib import admin
from projects.models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'teamlead', 'mentor', 'open', 'organization')
    list_filter = ('id', 'name', 'open', 'mentor')
    search_fields = ('id', 'name', 'mentor')


admin.site.register(Project, ProjectAdmin)