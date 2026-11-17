# API de Estacionamento — Trabalho UFERSA

Implementação de API REST sobre o projeto-base `lisa-ufersa/django-quickproject`.

## Funcionalidades
- CRUD de clientes, veículos e vagas.
- Associação de veículos a clientes.
- Registro de entrada e saída, com data/hora automática.
- Cálculo da permanência em segundos e formato HH:MM:SS.
- Liberação automática da vaga após a saída.
- Bloqueio de entrada duplicada e ocupação simultânea da mesma vaga.
- Histórico de estadias, consulta de veículos ativos e resumo de vagas.

## Instalação (na pasta já clonada `~/api-estacionamento`)

1. Extraia o ZIP e copie a pasta `estacionamento` e o arquivo `aplicar_no_projeto.py` para dentro da pasta do projeto, ao lado de `manage.py`.
2. Instale as dependências do projeto-base (caso necessário):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Aplique as alterações de configuração e prepare o banco:

```bash
python aplicar_no_projeto.py
python manage.py makemigrations estacionamento
python manage.py migrate
python manage.py test estacionamento
python manage.py runserver
```

## Endpoints

| Método | Rota | Função |
|---|---|---|
| GET/POST | `/api/clientes/` | Listar/cadastrar clientes |
| GET/PUT/PATCH/DELETE | `/api/clientes/{id}/` | Gerenciar cliente |
| GET/POST | `/api/veiculos/` | Listar/cadastrar veículos |
| GET/POST | `/api/vagas/` | Listar/cadastrar vagas |
| GET | `/api/vagas/disponiveis/` | Listar vagas livres |
| POST | `/api/entrada/` | Registrar entrada |
| POST | `/api/saida/` | Registrar saída |
| GET | `/api/estadias/` | Histórico completo |
| GET | `/api/estadias/ativos/` | Veículos estacionados |
| GET | `/api/resumo/` | Quantidade de vagas totais, ocupadas e livres |

## Exemplo de uso

Cadastre cliente:

```json
{"nome":"Ana Silva","cpf":"12345678901","telefone":"84999999999"}
```

Cadastre veículo (supondo cliente ID 1):

```json
{"cliente":1,"placa":"ABC1D23","marca":"Fiat","modelo":"Uno","cor":"Branco"}
```

Cadastre vaga:

```json
{"numero":"V01","ativa":true}
```

Registre entrada (supondo veículo ID 1 e vaga ID 1):

```json
{"veiculo":1,"vaga":1}
```

Registre saída:

```json
{"veiculo":1}
```

A resposta da saída inclui `entrada`, `saida`, `duracao_segundos` e `tempo_formatado`.

## Observações
- CPF: validação de formato (11 dígitos), não de dígitos verificadores.
- A API é um protótipo acadêmico, sem cobrança ou autenticação adicional específica nos novos endpoints.
- A base SQLite é suficiente para demonstração local. Em produção, adotar banco e bloqueios adequados à concorrência.
- Não envie `.venv`, banco local com dados pessoais ou credenciais para o GitHub.
