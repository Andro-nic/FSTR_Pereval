from rest_framework import serializers

from .models import Pereval, User, Coords, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'last_name', 'first_name', 'middle_name']


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image', 'title']


class PerevalSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    images = ImageSerializer(many=True)

    class Meta:
        model = Pereval
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        coords_data = validated_data.pop('coords')
        images_data = validated_data.pop('images')

        user = User.objects.create(**user_data)
        coords = Coords.objects.create(**coords_data)
        pereval = Pereval.objects.create(user=user, coords=coords, **validated_data)

        for image_data in images_data:
            Image.objects.create(pereval=pereval, **image_data)

        return pereval