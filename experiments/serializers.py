from rest_framework import serializers

from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    """ Serializer of the Place model.

    """

    pagination_class = None
    img_link = serializers.ReadOnlyField(source='path_img')

    class Meta:
        model = Image
        fields = ["id", "name", "clase", "img_link"]
