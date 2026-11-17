from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (ClienteViewSet, VeiculoViewSet, VagaViewSet,
                    EstadiaViewSet, registrar_entrada, registrar_saida, resumo)

router = DefaultRouter()
router.register('clientes', ClienteViewSet)
router.register('veiculos', VeiculoViewSet)
router.register('vagas', VagaViewSet)
router.register('estadias', EstadiaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('entrada/', registrar_entrada),
    path('saida/', registrar_saida),
    path('resumo/', resumo),
]
