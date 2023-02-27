from django.http.response import JsonResponse
# from django.views.generic import View
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .serializers import ImageSerializer
from . import models


# Create your views here.


class Images(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """ GET request Get all the places.

        Args:
            request:
            lang:

        Returns:

        """
        images = models.Image.objects.all()
        images_serializer = ImageSerializer(images, many=True)

        return JsonResponse(images_serializer.data, safe=False)