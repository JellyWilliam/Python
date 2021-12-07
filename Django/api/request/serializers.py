from rest_framework import serializers

from main.models import Request
from ..main.serializers import ManagingOrganizationSerializer, WorkerSerializer


class RequestSerializer(serializers.ModelSerializer):

    observing = WorkerSerializer()
    manage_org = ManagingOrganizationSerializer()

    class Meta:
        model = Request
        fields = '__all__'
