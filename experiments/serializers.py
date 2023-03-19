from rest_framework import serializers

from . import models


class ImageSerializer(serializers.ModelSerializer):
    """ Serializer of the Place model.

    """
    img_link = serializers.ReadOnlyField(source='path_img')
    img_org_link = serializers.ReadOnlyField(source='path_img_org')

    class Meta:
        model = models.Image
        fields = ["id", "name", "clase", "img_link", "img_org_link"]


class AnswerSerializer(serializers.ModelSerializer):
    """ Serializer of the Place model.

    """
    class Meta:
        model = models.Answer
        fields = ["start_time", "end_time", "trust"]