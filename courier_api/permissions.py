from rest_framework.permissions import BasePermission

class CanCreateParcel(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Customer" or request.user.role == "Admin"
    

class CanViewParcelStatus(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.reciever or request.user == obj.courier or request.user.role == "Admin"
    
class CanConfirmDelivery(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.reciever and obj.status == "Pre delivery"
    
class CanConfirmPreDelivery(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.courier

class CanDeleteParcel(BasePermission):
    ...

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Admin"
    
class IsCourier(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Courier"


class CanUpdateParcelStatus(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.status in ["Pending", "In Transit"],request.user == obj.courier or request.user.role == "Admin"
    
class CanUploadDeliveryProof(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.courier or request.user.role == "Admin"
    

class CanAssignParcel(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.role == "Courier" and obj.status == 'Pending') or request.user.role == "Admin"
