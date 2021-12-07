from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404

from .serializers import TarifPaySerializer, WorkerSerializer
from ..AdressTarif.serializers import  TarifBuildSerializer
from main.models import *


class TarifPayViewSet(ModelViewSet):

    serializer_class = TarifPaySerializer
    queryset = TarifPay.objects.all()

    @staticmethod
    def get_tarif(location):
        if location:
            return TarifPay.objects.filter(location=location).first()
        return 'Введите населенный пункт'


class TarifBuildViewSet(ModelViewSet):

    serializer_class = TarifBuildSerializer
    queryset = TarifBuild.objects.all()


class WorkerViewSet(ModelViewSet):

    serializer_class = WorkerSerializer
    queryset = Worker.objects.all()

    @staticmethod
    def get_worker(id):
        if id:
            return TarifPay.objects.filter(id=id).first()
        return 'Войдите в систему'
