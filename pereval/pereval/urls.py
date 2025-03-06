from django.urls import path
from .views import (PerevalCreateAPIView, PerevalDetailAPIView, PerevalUpdateAPIView, PerevalAPIView)


urlpatterns = [
    path('pereval/', PerevalAPIView.as_view(), name='pereval-list'),
    path('pereval/create/', PerevalCreateAPIView.as_view(), name='pereval-create'),
    path('pereval/<int:pk>/', PerevalDetailAPIView.as_view(), name='pereval-detail'),
    path('pereval/<int:pk>/update/', PerevalUpdateAPIView.as_view(), name='pereval-update'),
]
