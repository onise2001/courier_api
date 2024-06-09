from django.shortcuts import render
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
# Create your views here.

class CustomUserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


# class AuthView(ListAPIView):
#     queryset = CustomUser.objects.all()