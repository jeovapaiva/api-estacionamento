from rest_framework import serializers
from .models import Cliente, Veiculo, Vaga, Estadia


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'cpf', 'telefone']

    def validate_cpf(self, value):
        if not value.isdigit() or len(value) != 11:
            raise serializers.ValidationError('O CPF deve conter 11 dígitos numéricos.')
        return value


class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = ['id', 'cliente', 'placa', 'marca', 'modelo', 'cor']

    def validate_placa(self, value):
        value = value.upper().strip().replace('-', '')
        if len(value) != 7 or not value.isalnum():
            raise serializers.ValidationError('A placa deve ter 7 caracteres alfanuméricos.')
        return value


class VagaSerializer(serializers.ModelSerializer):
    disponivel = serializers.SerializerMethodField()

    class Meta:
        model = Vaga
        fields = ['id', 'numero', 'ativa', 'disponivel']

    def get_disponivel(self, obj):
        return obj.ativa and not obj.estadias.filter(saida__isnull=True).exists()


class EstadiaSerializer(serializers.ModelSerializer):
    tempo_formatado = serializers.ReadOnlyField()

    class Meta:
        model = Estadia
        fields = ['id', 'veiculo', 'vaga', 'entrada', 'saida', 'duracao_segundos', 'tempo_formatado']
        read_only_fields = fields


class EntradaSerializer(serializers.Serializer):
    veiculo = serializers.PrimaryKeyRelatedField(queryset=Veiculo.objects.all())
    vaga = serializers.PrimaryKeyRelatedField(queryset=Vaga.objects.filter(ativa=True))


class SaidaSerializer(serializers.Serializer):
    veiculo = serializers.PrimaryKeyRelatedField(queryset=Veiculo.objects.all())
