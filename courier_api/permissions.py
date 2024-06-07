from rest_framework.permissions import BasePermission

class CanCreateParcel(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Customer" or request.user.role == "Admin"
    

class CanViewParcelStatus(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.reciever or request.user == obj.courier or request.user.role == "Admin"
    
class CanDeleteParcel(BasePermission):
    ...

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Admin"

class CanConfirmDelivery(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.reciver or request.user.role == "Admin"

    

class CanUpdateParcelStatus(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.courier or request.user.role == "Admin"
    
class CanUploadDeliveryProof(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.courier or request.user.role == "Admin"
    

class CanAssignParcel(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.role == "Courier" and obj.status == 'Pending'
