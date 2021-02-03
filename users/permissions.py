from rest_framework import permissions


class IsStudent(permissions.BasePermission):
    message = 'Only students can access this feature.'

    def has_permission(self, request, view):
        return not request.user.is_expert


class IsAdmin(permissions.BasePermission):
    message = 'Only admins can access this feature.'

    def has_permission(self, request, view):
        return request.user.is_superuser


class EmailVerified(permissions.BasePermission):
    message = 'Email verification required.'

    def has_permission(self, request, view):
        return request.user.verified


class ProfileCompleted(permissions.BasePermission):
    message = 'Profile completion required.'

    def has_permission(self, request, view):
        return request.user.profile_completed
