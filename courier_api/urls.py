from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParcelViewSet, AssingParcelView, AdminAssignParcelView,AllPendingParcelsView, MarkParcelAsPreDelivered, MyParcelsView, CourierParcelsView, ConfirmDelivery

router = DefaultRouter(trailing_slash=False)
router.register(r'parcel', ParcelViewSet)
router.register(r'mark_pre_delivered/', MarkParcelAsPreDelivered)

urlpatterns = [
    path('', include(router.urls)),
    path('assign_parcel/<int:pk>', AssingParcelView.as_view()),
    path('admin_assign_parcel/<int:pk>', AdminAssignParcelView.as_view()),
    path('pending_parcels/', AllPendingParcelsView.as_view()),
    path('my_parcels/', MyParcelsView.as_view()),
    path('courier_parcels/',CourierParcelsView.as_view() ),
    path('mark_delivered/<int:pk>', ConfirmDelivery.as_view()),
    #path('mark_delivered/', MarkParcelAsDelivered.as_view()),
    

]
