from rest_framework import viewsets
from .models import User, Coords, Pereval, Image
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from django.db import DatabaseError
from .serializers import UserSerializer, CoordsSerializer, PerevalSerializer, ImageSerializer, PerevalCreateSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CoordsViewSet(viewsets.ModelViewSet):
    queryset = Coords.objects.all()
    serializer_class = CoordsSerializer

class PerevalViewSet(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class PerevalCreateAPIView(CreateAPIView):
    serializer_class = PerevalCreateSerializer

    def post(self, request, *args, **kwargs):
        pereval_serializer = self.get_serializer(data=request.data)
        try:
            if pereval_serializer.is_valid(raise_exception=True):
                pereval = pereval_serializer.save()
                return Response({
                    "status": status.HTTP_200_OK,
                    'message': 'Перевал успешно создан!',
                    "id": pereval.id
                }, status=status.HTTP_200_OK)

        except DatabaseError as db_err:
            # Обработка ошибок базы данных
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(db_err),
                "id": None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            # Обработка других ошибок
            return Response({
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
                "id": None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Если данные не валидны, вернуть ошибку валидации
        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "message": pereval_serializer.errors,
            "id": None
        }, status=status.HTTP_400_BAD_REQUEST)