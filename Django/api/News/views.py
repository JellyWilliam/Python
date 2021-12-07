from rest_framework.viewsets import ModelViewSet

from .serializers import NewsSerializer
from main.models import News


class NewsViewSet(ModelViewSet):

    serializer_class = NewsSerializer
    queryset = News.objects.all()