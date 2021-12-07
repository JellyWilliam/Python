from rest_framework import routers

from ..request.views import RequestViewSet
from ..News.views import NewsViewSet
from .views import TarifPayViewSet, WorkerViewSet, TarifBuildViewSet


router = routers.SimpleRouter()
router.register('request', RequestViewSet, basename='request')
router.register('tarif', TarifPayViewSet, basename='tarif')
router.register('worker', WorkerViewSet, basename='worker')
router.register('tarif_build', TarifBuildViewSet, basename='tarif_build')
router.register('news', NewsViewSet, basename='news')

urlpatterns = []
urlpatterns += router.urls
