from rest_framework import serializers

from main.models import ManagingOrganization, Worker, TarifPay


class ManagingOrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = ManagingOrganization
        fields = '__all__'


class TarifPaySerializer(serializers.ModelSerializer):

    class Meta:
        model = TarifPay
        fields = '__all__'


class WorkerSerializer(serializers.ModelSerializer):

    observing = serializers.SerializerMethodField()

    class Meta:
        model = Worker
        fields = '__all__'

    @staticmethod
    def get_observing(obj):
        return ' '.join([obj.observing.first_name, obj.observing.last_name])
