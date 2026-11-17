from django.test import TestCase
from rest_framework.test import APIClient
from .models import Cliente, Veiculo, Vaga, Estadia


class FluxoEstacionamentoTests(TestCase):
    def setUp(self):
        self.api = APIClient()
        self.cliente = Cliente.objects.create(nome='Ana', cpf='12345678901')
        self.carro = Veiculo.objects.create(cliente=self.cliente, placa='ABC1D23', marca='Fiat', modelo='Uno')
        self.vaga = Vaga.objects.create(numero='V01')

    def test_fluxo_entrada_saida_e_liberacao(self):
        entrada = self.api.post('/api/entrada/', {'veiculo': self.carro.pk, 'vaga': self.vaga.pk})
        self.assertEqual(entrada.status_code, 201)
        self.assertEqual(self.api.get('/api/resumo/').data['disponiveis'], 0)
        self.assertEqual(self.api.get('/api/vagas/disponiveis/').data, [])
        saida = self.api.post('/api/saida/', {'veiculo': self.carro.pk})
        self.assertEqual(saida.status_code, 200)
        self.assertIsNotNone(saida.data['duracao_segundos'])
        self.assertEqual(self.api.get('/api/resumo/').data['disponiveis'], 1)

    def test_nao_aceita_entrada_duplicada(self):
        dados = {'veiculo': self.carro.pk, 'vaga': self.vaga.pk}
        self.assertEqual(self.api.post('/api/entrada/', dados).status_code, 201)
        self.assertEqual(self.api.post('/api/entrada/', dados).status_code, 400)

    def test_nao_aceita_vaga_ocupada(self):
        outro = Veiculo.objects.create(cliente=self.cliente, placa='XYZ9A87', marca='VW', modelo='Gol')
        self.api.post('/api/entrada/', {'veiculo': self.carro.pk, 'vaga': self.vaga.pk})
        self.assertEqual(self.api.post('/api/entrada/', {'veiculo': outro.pk, 'vaga': self.vaga.pk}).status_code, 400)

    def test_nao_aceita_saida_sem_entrada(self):
        self.assertEqual(self.api.post('/api/saida/', {'veiculo': self.carro.pk}).status_code, 400)

    def test_cadastro_cliente_e_veiculo(self):
        self.assertEqual(self.api.get('/api/clientes/').status_code, 200)
        self.assertEqual(self.api.get('/api/veiculos/').status_code, 200)
