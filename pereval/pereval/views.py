from .models import Pereval
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, ListAPIView
from django.db import DatabaseError
from .serializers import PerevalSerializer, PerevalUpdateSerializer, PerevalCreateSerializer


# GET api/pereval/<int:pk> - извлекает конкретную запись по её id и включает всю связанную информацию,
# включая статус модерации.
class PerevalDetailAPIView(RetrieveAPIView):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer


# GET api/pereval/?user__email=<emailList> - фильтрует по email
class PerevalAPIView(ListAPIView):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer
    filterset_fields = ('user__email',)



# POST api/pereval/create - добавляет перевел
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


# PATCH api/pereval/<int:pk>/update - обновляет перевал
class PerevalUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = PerevalUpdateSerializer

    def get_queryset(self):
        return Pereval.objects.all()

    def patch(self, request, *args, **kwargs):
        pereval = self.get_object()  # Получаем объект

        # Проверяем статус объекта
        if pereval.status != 'NE':
            return Response({"state": 0, "message": "Нельзя редактировать запись, не находящуюся в статусе 'new'"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Проверяем наличие поля 'user' в запросе
        if 'user' in request.data:
            return Response({"state": 0, "message": "Нельзя редактировать поля объекта 'user'"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Обработка обновления объекта
        serializer = self.get_serializer(pereval, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({"state": 1, "message": "Запись успешно отредактирована", "data": serializer.data})
