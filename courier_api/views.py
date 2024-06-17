from django.shortcuts import render
from .models import Parcel, DeliveryProof
from .serializers import ParcelSerializer, DeliverySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView, ListAPIView
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from .permissions import CanViewParcelStatus, CanCreateParcel, CanUpdateParcelStatus, IsAdmin, IsCourier, CanAssignParcel, CanConfirmPreDelivery, CanConfirmDelivery, IsCustomer,CanUpdateParcel
from .filters import MyParcelsFilter, PendingParcelsFilter, CourierParcelsFilter
from rest_framework.response import Response
from rest_framework import status
from users.models import CustomUser

# Create your views here.

class ParcelViewSet(ModelViewSet):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    filter_backends = [MyParcelsFilter]


    def perform_create(self, serializer):
        serializer.save(reciever=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            #print('in list permissions')
            permission_classes = [IsCustomer]
        elif self.action == 'create':
            permission_classes = [CanCreateParcel]
        elif self.action in ['update', 'partial_update']:
            #print(self.request.user)
            permission_classes = [IsAuthenticated & CanUpdateParcel]
        else:
            permission_classes = [IsAdmin]
        
        return [permission() for permission in permission_classes]


class AllPendingParcelsView(ListAPIView):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    filter_backends = [PendingParcelsFilter]
    permission_classes = [IsAdmin | IsCourier]



class AdminAssignParcelView(UpdateAPIView):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        parcel = self.get_object()
        courier = CustomUser.objects.get(pk=request.data['courier'])
        if courier:
            parcel.courier = courier
            parcel.status = "In Transit"
            parcel.save()
            serializer = self.serializer_class(parcel)
            return Response(serializer.data,status=status.HTTP_200_OK)
        




class AssingParcelView(UpdateAPIView):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    permission_classes = [CanAssignParcel]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        parcel = self.get_object()
        parcel.courier = request.user
        parcel.status = "In Transit"
        parcel.save()
        serializer = self.serializer_class(parcel)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class MyParcelsView(ListAPIView):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [MyParcelsFilter]



class MarkParcelAsPreDelivered(ModelViewSet):
    queryset = DeliveryProof.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [CanConfirmPreDelivery]



class ConfirmDelivery(UpdateAPIView):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    permission_classes = [CanConfirmDelivery]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        parcel = self.get_object()
        self.check_object_permissions(request, parcel)
        parcel.status = 'Delivered'
        parcel.save()
        serializer = self.serializer_class(parcel)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CourierParcelsView(ListAPIView):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [CourierParcelsFilter]