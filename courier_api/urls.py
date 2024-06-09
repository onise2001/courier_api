from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParcelViewSet, AssingParcelView, AdminAssignParcelView,AllPendingParcelsView, MarkParcelAsDelivered

router = DefaultRouter(trailing_slash=False)
router.register(r'parcel', ParcelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('assign_parcel/', AssingParcelView.as_view()),
    path('admin_assign_parcel/', AdminAssignParcelView.as_view()),
    path('pending_parcels/', AllPendingParcelsView.as_view()),
    path('mark_delivered/', MarkParcelAsDelivered.as_view()),
    

]
