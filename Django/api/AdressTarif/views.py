from rest_framework.viewsets import ModelViewSet

from serializers import AdressForTarifSerializer, TarifBuildSerializer
from main.models import AdressForTarif, TarifBuild


class AdressForTarifViewSet(ModelViewSet):

    serializer_class = AdressForTarifSerializer
    queryset = AdressForTarif.objects.all()


class TarifBuildViewSet(ModelViewSet):

    serializer_class = TarifBuildSerializer
    queryset = TarifBuild.objects.all()
