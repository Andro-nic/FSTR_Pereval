from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CoordsViewSet, PerevalViewSet, ImageViewSet, PerevalCreateView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'coords', CoordsViewSet)
router.register(r'perevals', PerevalViewSet)
router.register(r'images', ImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('pereval/create/', PerevalCreateView.as_view(), name='pereval-create'),  # Маршрут для APIView
]