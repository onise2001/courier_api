from django.shortcuts import render
from .models import Parcel, DeliveryProof
from .serializers import ParcelSerializer, DeliverySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import UpdateAPIView 
from rest_framework.permissions import SAFE_METHODS
from .permissions import CanViewParcelStatus, CanCreateParcel, CanUpdateParcelStatus, IsAdmin, CanAssignParcel
from .filters import MyParcelsFilter
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class ParcelViewSet(ModelViewSet):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    filter_backends = [MyParcelsFilter]


    def get_permissions(self):
        if self.action in SAFE_METHODS:
            permission_classes = [CanViewParcelStatus]
        elif self.action == 'create':
            permission_classes = [CanCreateParcel]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [CanUpdateParcelStatus]
        #elif self.action == 'destroy':
        else:
            permission_classes = [IsAdmin]
        
        return [permission() for permission in permission_classes]



class AssingParcelView(UpdateAPIView):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    permission_classes = [CanAssignParcel]
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        parcel = self.get_object()
        serializer = self.serializer_class(instance=parcel, data={'courier': request.user}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




