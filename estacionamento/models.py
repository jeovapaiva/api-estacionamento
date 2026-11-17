from django.db import models
from django.utils import timezone


class Cliente(models.Model):
    nome = models.CharField(max_length=120)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nome


class Veiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='veiculos')
    placa = models.CharField(max_length=7, unique=True)
    marca = models.CharField(max_length=60)
    modelo = models.CharField(max_length=60)
    cor = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.placa


class Vaga(models.Model):
    numero = models.CharField(max_length=20, unique=True)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.numero


class Estadia(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, related_name='estadias')
    vaga = models.ForeignKey(Vaga, on_delete=models.PROTECT, related_name='estadias')
    entrada = models.DateTimeField(default=timezone.now)
    saida = models.DateTimeField(null=True, blank=True)
    duracao_segundos = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-entrada']
        constraints = [
            models.UniqueConstraint(fields=['veiculo'], condition=models.Q(saida__isnull=True), name='veiculo_estadia_aberta_unica'),
            models.UniqueConstraint(fields=['vaga'], condition=models.Q(saida__isnull=True), name='vaga_estadia_aberta_unica'),
        ]

    @property
    def tempo_formatado(self):
        if self.duracao_segundos is None:
            return None
        horas, resto = divmod(self.duracao_segundos, 3600)
        minutos, segundos = divmod(resto, 60)
        return f'{horas:02d}:{minutos:02d}:{segundos:02d}'
