from rest_framework import permissions, status

class IsAdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS: #here SAFE_METHODS are GET, HEAD, OPTIONS, TRACE
            return True
        else:
            return bool(request.user and request.user.is_staff) #check if user is admin or staff
 
class IsReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: #check permission for read only requests
            return True
        else:
            return obj.review_user == request.user or request.user.is_staff #check permission for writr request and if user is the same as review user so he can update or delete the review 