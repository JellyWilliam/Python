from rest_framework import serializers

from main.models import News


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = '__all__'
