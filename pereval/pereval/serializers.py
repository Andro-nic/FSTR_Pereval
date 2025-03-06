from rest_framework import serializers
from .models import Pereval, User, Coords, Image, Levels


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
        fields = '__all__'
        #fields = ['level_spring', 'level_summer', 'level_autumn', 'level_winter']

class LevelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Levels
        fields = '__all__'
        #fields = ['latitude', 'longitude', 'height']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['data', 'title',]


class PerevalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    levels = LevelsSerializer()
    images = ImageSerializer(many=True)


    class Meta:
        model = Pereval
        fields = '__all__'


class PerevalCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    levels = LevelsSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Pereval
        fields = ['beauty_title', 'title', 'other_titles', 'connect', 'user', 'coords', 'levels', 'images']

    def create(self, validated_data):

        user_data = validated_data.pop('user', None)
        coords_data = validated_data.pop('coords', None)
        levels_data = validated_data.pop('levels', None)
        images_data = validated_data.pop('images')
        # Проверяем обязательные данные
        if user_data is None or coords_data is None:
            raise ValueError("User and Coords data must be provided.")
        # Проверяем существование пользователя по email
        user_email = user_data.get('email')
        user = User.objects.filter(email=user_email).first()
        if not user:
            # Если пользователь не существует, создаем нового
            user = User.objects.create(**user_data)
        # Создаем объекты Coords и Levels
        coords = Coords.objects.create(**coords_data)
        levels = Levels.objects.create(**levels_data)
        # Создаем объект Pereval
        pereval = Pereval.objects.create(user=user, coords=coords, levels=levels, **validated_data)
        # Создаем связанные изображения
        for image in images_data:
            data = image.pop('data')
            title = image.pop('title')
            Image.objects.create(pereval=pereval, title=title, data=data)

        return pereval


class PerevalUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    levels = LevelsSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Pereval
        fields =  ['beauty_title', 'title', 'other_titles', 'connect', 'user', 'coords', 'levels', 'images']

    def update(self, instance, validated_data):

        coords_data = validated_data.pop('coords', None)
        levels_data = validated_data.pop('levels', None)
        images_data = validated_data.pop('images', None)
        # Обновляем обычные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if coords_data:
            for attr, value in coords_data.items():
                setattr(instance.coords, attr, value)
            instance.coords.save()

        if levels_data:
            for attr, value in levels_data.items():
                setattr(instance.levels, attr, value)
            instance.levels.save()

        # Обновляем изображения только если новые изображения переданы
        if images_data is not None:
            # Удаляем старые изображения
            instance.images.all().delete()
            for image_data in images_data:
                data = image_data.pop('data')
                title = image_data.pop('title')
                Image.objects.create(pereval=instance, title=title, data=data)

        instance.save()
        return instance
