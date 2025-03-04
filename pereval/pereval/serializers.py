from rest_framework import serializers
from .models import Pereval, User, Coords, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'last_name', 'first_name', 'middle_name']

    def to_internal_value(self, data):
        data = data.copy()
        # Переопределяем только если данные приходят с полями 'fam', 'name' и 'otc'
        if 'fam' in data:
            data['last_name'] = data.pop('fam')
        if 'name' in data:
            data['first_name'] = data.pop('name')
        if 'otc' in data:
            data['middle_name'] = data.pop('otc')

        return super().to_internal_value(data)


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['data', 'title',]


class PerevalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Pereval
        fields = '__all__'


class PerevalCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Pereval
        fields = ['beauty_title', 'title', 'other_titles', 'connect', 'user', 'coords', 'images', 'level_spring',
                  'level_summer', 'level_autumn', 'level_winter']

    def create(self, validated_data):

        user_data = validated_data.pop('user', None)
        coords_data = validated_data.pop('coords', None)
        images_data = validated_data.pop('images')

        # Проверяем обязательные данные
        if user_data is None or coords_data is None:
            raise ValueError("User and Coords data must be provided.")

        # Создаем объекты
        user = User.objects.create(**user_data)
        coords = Coords.objects.create(**coords_data)
        pereval = Pereval.objects.create(user=user, coords=coords, **validated_data)

        for image in images_data:
            data = image.pop('data')
            title = image.pop('title')
            Image.objects.create(pereval=pereval, title=title, data=data)

        return pereval


class PerevalUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Pereval
        fields = ['user', 'coords', 'images', 'beauty_title', 'title', 'other_titles', 'connect', 'level_spring',
                  'level_summer', 'level_autumn', 'level_winter']

    def update(self, instance, validated_data):

        coords_data = validated_data.pop('coords', None)
        images_data = validated_data.pop('images', None)
        # Обновляем обычные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if coords_data:
            for attr, value in coords_data.items():
                setattr(instance.coords, attr, value)
            instance.coords.save()

        # Обновляем изображения
        if images_data is not None:
            # Удаляем старые изображения, если они не переданы
            instance.images.all().delete()
            for image_data in images_data:
                data = image_data.pop('data')
                title = image_data.pop('title')
                Image.objects.create(pereval=instance, title=title, data=data)

        instance.save()
        return instance
