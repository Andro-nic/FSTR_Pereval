from django.urls import path
from .views import (PerevalCreateAPIView, PerevalDetailAPIView, PerevalUpdateAPIView, PerevalAPIView)


urlpatterns = [
    path('add_pereval/', PerevalAPIView.as_view(), name='add_pereval-list'),
    path('add_pereval/create/', PerevalCreateAPIView.as_view(), name='add_pereval-create'),
    path('add_pereval/<int:pk>/', PerevalDetailAPIView.as_view(), name='add_pereval-detail'),
    path('add_pereval/<int:pk>/update/', PerevalUpdateAPIView.as_view(), name='add_pereval-update'),
]
