from rest_framework import permissions


class IsProjectOwnerOrInviter(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True

            return request.user.id == obj.teamlead.id or request.user.id in obj.invites

        return False


class IsProjectOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True

            return request.user.id == obj.teamlead.id

        return False
