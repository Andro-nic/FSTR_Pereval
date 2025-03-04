from django.urls import path, include
from .views import ( PerevalCreateAPIView, PerevalDetailAPIView, PerevalUpdateAPIView, PerevalListByEmailAPIView )



urlpatterns = [
    path('pereval/create/', PerevalCreateAPIView.as_view(), name='pereval-create'),  # Маршрут для APIView
    path('pereval/<int:pk>/', PerevalDetailAPIView.as_view(), name='pereval-detail'),
    path('pereval/<int:pk>/update/', PerevalUpdateAPIView.as_view(), name='pereval-update'),
    path('pereval/', PerevalListByEmailAPIView.as_view(), name='pereval-list-by-email'),
]