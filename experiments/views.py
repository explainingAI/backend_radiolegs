from datetime import datetime

from django.db.models import Q
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status

from . import models
from .serializers import ImageSerializer, AnswerSerializer


class Images(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """ GET request Get all the places.

        Args:
            request:

        Returns:

        """
        usuari = request.user
        exp = models.Experiment.objects.get(user=usuari)

        images = models.Image.objects.filter(
            Q(answer__experiment=exp) & Q(answer__trust__isnull=True)).all()

        images_serializer = ImageSerializer(images, many=True)

        return JsonResponse(images_serializer.data, safe=False)


class Answer(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        usuari = request.user
        exp = models.Experiment.objects.get(user=usuari)
        image = models.Image.objects.get(pk=pk)

        answ = models.Answer.objects.filter(Q(image=image) & Q(experiment=exp)).get()

        request.data['end_time'] = datetime.fromtimestamp(request.data['end_time']/1000)
        request.data['start_time'] = datetime.fromtimestamp(request.data['start_time']/1000)

        serializer = AnswerSerializer(answ, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)