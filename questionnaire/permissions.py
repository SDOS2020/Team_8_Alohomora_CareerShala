from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    message = 'Only students can access questionnaires.'

    def has_permission(self, request, view):
        return not request.user.is_expert
