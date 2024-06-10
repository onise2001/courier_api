from django.db import models
from users.models import CustomUser
# Create your models here.


class Parcel(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'pending'),
        ('In Transit', 'in transit'),
        ('Pre delivery', 'pre delivery'),
        ('Delivered', 'delivered'),
    )


    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=100, default="Pending",choices=STATUS_CHOICES, )
    reciever = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reciver')
    reciever_name = models.CharField(max_length=100)
    reciever_address = models.TextField()
    courier = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='courier', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True)


class DeliveryProof(models.Model):
    parcel = models.OneToOneField(Parcel, on_delete=models.CASCADE)
    image = models.ImageField()
    timestamp = models.DateTimeField(auto_now_add=True)