from django.contrib import admin
from projects.models import *


class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    list_filter = ('id', 'name')


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('id', 'speciality', 'open', 'description')
    search_fields = ('id', 'speciality')
    list_filter = ('id', 'open')


class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'vacancy')
    search_fields = ('id', 'user', 'vacancy')
    list_filter = ('id',)


class IncomingApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_from', 'project', 'vacancy', 'annotation')
    search_fields = ('id', 'user_from')
    list_filter = ('id',)


class OutcomingApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_to', 'project', 'vacancy')
    search_fields = ('id', 'user_to', 'project')
    list_filter = ('id',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'branch', 'teamlead', 'approved', 'cover')
    search_fields = ('id', 'name')
    list_filter = ('id',)


admin.site.register(Branch, BranchAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(IncomingApplication, IncomingApplicationAdmin)
admin.site.register(OutgoingApplication, OutcomingApplicationAdmin)
admin.site.register(Project, ProjectAdmin)