from django.db import IntegrityError, transaction
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Cliente, Veiculo, Vaga, Estadia
from .serializers import (ClienteSerializer, VeiculoSerializer, VagaSerializer,
                          EstadiaSerializer, EntradaSerializer, SaidaSerializer)


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('id')
    serializer_class = ClienteSerializer


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.select_related('cliente').all().order_by('id')
    serializer_class = VeiculoSerializer


class VagaViewSet(viewsets.ModelViewSet):
    queryset = Vaga.objects.all().order_by('numero')
    serializer_class = VagaSerializer

    @action(detail=False, methods=['get'])
    def disponiveis(self, request):
        vagas = self.get_queryset().filter(ativa=True).exclude(estadias__saida__isnull=True)
        return Response(self.get_serializer(vagas, many=True).data)


class EstadiaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Estadia.objects.select_related('veiculo', 'vaga').all()
    serializer_class = EstadiaSerializer

    @action(detail=False, methods=['get'])
    def ativos(self, request):
        return Response(self.get_serializer(self.get_queryset().filter(saida__isnull=True), many=True).data)


@api_view(['POST'])
def registrar_entrada(request):
    serializer = EntradaSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    veiculo, vaga = serializer.validated_data['veiculo'], serializer.validated_data['vaga']
    try:
        with transaction.atomic():
            if Estadia.objects.filter(veiculo=veiculo, saida__isnull=True).exists():
                return Response({'erro': 'Veículo já está estacionado.'}, status=status.HTTP_400_BAD_REQUEST)
            if Estadia.objects.filter(vaga=vaga, saida__isnull=True).exists():
                return Response({'erro': 'Vaga ocupada.'}, status=status.HTTP_400_BAD_REQUEST)
            estadia = Estadia.objects.create(veiculo=veiculo, vaga=vaga)
    except IntegrityError:
        return Response({'erro': 'Veículo ou vaga indisponível.'}, status=status.HTTP_409_CONFLICT)
    return Response(EstadiaSerializer(estadia).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def registrar_saida(request):
    serializer = SaidaSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    veiculo = serializer.validated_data['veiculo']
    with transaction.atomic():
        estadia = Estadia.objects.select_for_update().filter(veiculo=veiculo, saida__isnull=True).first()
        if not estadia:
            return Response({'erro': 'Veículo não possui entrada em aberto.'}, status=status.HTTP_400_BAD_REQUEST)
        agora = timezone.now()
        estadia.saida = agora
        estadia.duracao_segundos = max(0, int((agora - estadia.entrada).total_seconds()))
        estadia.save(update_fields=['saida', 'duracao_segundos'])
    return Response(EstadiaSerializer(estadia).data)


@api_view(['GET'])
def resumo(request):
    total = Vaga.objects.filter(ativa=True).count()
    ocupadas = Estadia.objects.filter(saida__isnull=True, vaga__ativa=True).count()
    return Response({'total_vagas': total, 'ocupadas': ocupadas, 'disponiveis': total - ocupadas})
