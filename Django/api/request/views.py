from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .serializers import RequestSerializer
from main.models import *


class RequestViewSet(ModelViewSet):

    serializer_class = RequestSerializer
    queryset = Request.objects.all()

    @staticmethod
    def get_request(observing):
        if observing.is_authenticated:
            return Request.objects.filter(observing=observing.worker).first()
        return 'Авторизируйтесь'

    @action(methods=['get'], detail=False)
    def current_worker_request(self, *args, **kwargs):
        request = self.get_request(self.request.user)
        request_serializer = RequestSerializer(request)
        return Response(request_serializer.data)
