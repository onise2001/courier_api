from rest_framework import serializers
from .models import Parcel, DeliveryProof
from users.serializers import CustomUserSerializer
from users.models import CustomUser

class ParcelSerializer(serializers.ModelSerializer):
    reciever = CustomUserSerializer(read_only=True)
    courier = CustomUserSerializer(read_only=True)


    class Meta:
        model = Parcel
        fields = '__all__'



    def create(self, validated_data):
        reciever = validated_data.pop('reciever')
        parcel = Parcel(**validated_data)
        parcel.reciever = reciever
        parcel.save()
        return parcel

class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryProof
        fields = '__all__'
    

    def create(self, validated_data):
        parcel = Parcel.objects.get(pk=validated_data.get('parcel').id)
        print(parcel)
        if parcel:
            delivery = DeliveryProof.objects.create(**validated_data)
            parcel.status = 'Pre delivery'
            parcel.save()
            return delivery
        
        raise serializers.ValidationError("No such parcel")

