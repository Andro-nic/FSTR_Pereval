from rest_framework import viewsets
from .models import User, Coords, Pereval, Image
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView
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
                pereval_serializer.save()
                data = {'status': '200', 'message': 'null', 'id': f'{pereval_serializer.instance.id}'}
                return JsonResponse(data=data)

        except Exception as exc:
            data = {'status': '400', 'message': f'Bad Request: {exc}', 'id': 'null'}
            return JsonResponse(data=data)

