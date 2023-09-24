from rest_framework import permissions
from projects.models import Project


class IsTeamleadOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.pk == obj.teamlead.pk
    

class IsTeamleadApplicationAcceptReject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.pk == obj.project.teamlead.pk
    


class IsTeamleadApplicationSend(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.pk == Project.objects.get(pk=request.data['project']).teamlead.pk
    

class IsRecieverApplicationAcceptReject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.pk == obj.user_to.pk