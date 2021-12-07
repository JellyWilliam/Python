from django.shortcuts import render

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from .models import CustomUser
from .serializers import UserSerializer


class UserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


def index_view(request):
    return render(request, 'index.html', {})


def request_detail(request, id):
    return render(request, 'index.html', {})


def tarif_detail(request, location):
    return render(request, 'index.html', {})


def worker_detail(request, id):
    return render(request, 'index.html', {})
