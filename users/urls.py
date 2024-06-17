from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet

router = DefaultRouter(trailing_slash=True)
router.register(r'signup', CustomUserViewSet)

urlpatterns = [
     path('', include(router.urls)),
     path('login/', TokenObtainPairView.as_view(), name='login'),
     path('refresh/', TokenRefreshView.as_view()),
]

