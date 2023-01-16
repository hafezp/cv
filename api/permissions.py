
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperUser(BasePermission):
    """
    Allows access only to superuser.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):



        return bool(
        	# get access to superuser
        	request.user.is_authenticated and 

        	request.user.is_superuser or

        	# get access to author of objet

		obj.user == request.user                
        )
