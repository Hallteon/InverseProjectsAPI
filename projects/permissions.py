from rest_framework import permissions


class IsProjectOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True

            return request.user.id == obj.teamlead.id

        return False


class IsProjectInviter(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True

            return request.user.id in obj.invites.all()

        return False


class IsProjectClosedMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if (request.method in permissions.SAFE_METHODS and obj.open) or \
                    (request.method in permissions.SAFE_METHODS and not obj.open and request.user.id in obj.members.all()):

                return True

            return request.user.id == obj.teamlead.id

        return False


