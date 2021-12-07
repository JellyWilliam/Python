from rest_framework import serializers

from main.models import AdressForTarif, TarifBuild
from ..main.serializers import ManagingOrganizationSerializer


class AdressForTarifSerializer(serializers.ModelSerializer):

    manage_org = serializers.SerializerMethodField()

    class Meta:
        model = AdressForTarif
        fields = '__all__'


class TarifBuildSerializer(serializers.ModelSerializer):

    class Meta:
        model = TarifBuild
        fields = '__all__'
