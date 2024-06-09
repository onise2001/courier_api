from rest_framework import serializers
from .models import Parcel, DeliveryProof

class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = '__all__'

    
    def create(self, validated_data):
        parcel = Parcel.objects.get(pk=validated_data.get('parcel'))
        if parcel:
            delivery = DeliveryProof.objects.create(**validated_data)
            parcel.status = 'Delivered'
            parcel.save()
            return delivery
        
        raise serializers.ValidationError("No such parcel")





class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryProof
        fields = '__all__'
    


    def update(self, instance, validated_data):
        instance.courier = validated_data['courier']
        instance.save()
        return instance