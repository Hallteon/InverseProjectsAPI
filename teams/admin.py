from django.contrib import admin
from teams.models import Team


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'teamlead', 'mentor', 'open')
    list_filter = ('id', 'name', 'mentor', 'open')
    search_fields = ('id', 'name')


admin.site.register(Team, TeamAdmin)
