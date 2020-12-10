from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    message = 'Only students can access questionnaires.'

    def has_permission(self, request, view):
        return not request.user.is_expert


class EmailVerified(permissions.BasePermission):
    message = 'Email verification required.'

    def has_permission(self, request, view):
        return request.user.verified


class ProfileCompleted(permissions.BasePermission):
    message = 'Profile completion required.'

    def has_permission(self, request, view):
        return request.user.profile_completed
