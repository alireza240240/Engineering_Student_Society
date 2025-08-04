from rest_framework import permissions

class IsMemberOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: # yani SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            return True
        return request.user.is_authenticated and request.user.role in ['member','admin']
        
