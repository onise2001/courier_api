from rest_framework import serializers
from .models import Parcel, DeliveryProof

class ParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcel
        fields = '__all__'




class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryProof
        fields = '__all__'
    


    def update(self, instance, validated_data):
        instance.courier = validated_data['courier']
        instance.save()
        return instance