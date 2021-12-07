"""EDS1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from main.views import index_view, request_detail, tarif_detail, worker_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.main.router')),
    path('tarif/<str:location>/', tarif_detail),
    path('request/<int:id>/', request_detail),
    path('worker/<int:id>/', worker_detail),
    path('', index_view),
    path('api/v1/users/', include('main.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
