from rest_framework import serializers

from .models import Pereval, User, Coords, Image


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'phone', 'last_name', 'first_name', 'middle_name']

        class Meta:
            model = User
            fields = ['email', 'phone', 'fam', 'name', 'otc']

        def to_internal_value(self, data):
            data = data.copy()
            data['last_name'] = data.pop('fam', '')
            data['first_name'] = data.pop('name', '')
            data['middle_name'] = data.pop('otc', '')
            print("********")
            return super().to_internal_value(data)


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        fields = ['latitude', 'longitude', 'height']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['data', 'title']


class PerevalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pereval
        fields = '__all__'


class PerevalCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coords = CoordsSerializer()
    images = ImageSerializer(many=True)

    model = Pereval
    fields = ['beauty_title', 'title', 'other_titles', 'connect', 'user', 'coords', 'images', 'level_spring',
              'level_summer', 'level_autumn', 'level_winter']

    def create(self, validated_data):
        print("validated_data:", validated_data)

        user_data = validated_data.pop('user', None)  # Added None as default
        coords_data = validated_data.pop('coords', None)  # Added None as default
        images_data = validated_data.pop('images', [])

        if user_data is None or coords_data is None:
            raise ValueError("User and Coords data must be provided.")

        user = User.objects.create(**user_data)
        coords = Coords.objects.create(**coords_data)
        pereval = Pereval.objects.create(user=user, coords=coords, **validated_data)

        for image in images_data:
            data = image.pop('data')
            title = image.pop('title')
            Image.objects.create(pereval=pereval, title=title, data=data)

        return pereval




