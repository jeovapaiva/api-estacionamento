"""Execute este script na pasta raiz do django-quickproject."""
from pathlib import Path

settings = Path('config/settings.py')
urls = Path('config/urls.py')
if not settings.exists() or not urls.exists():
    raise SystemExit('Execute este script na raiz do projeto (onde existe manage.py).')
s = settings.read_text()
if '"estacionamento"' not in s and "'estacionamento'" not in s:
    marker = 'INSTALLED_APPS = ['
    if marker not in s:
        raise SystemExit('INSTALLED_APPS não encontrado; edite config/settings.py manualmente.')
    s = s.replace(marker, marker + '\n    "estacionamento",', 1)
    settings.write_text(s)
u = urls.read_text()
if 'estacionamento.urls' not in u:
    if 'from django.urls import ' in u:
        u = 'from django.urls import include as estacionamento_include, path as estacionamento_path\n' + u
    else:
        u = 'from django.urls import include as estacionamento_include, path as estacionamento_path\n' + u
    u += '\nurlpatterns += [estacionamento_path("api/", estacionamento_include("estacionamento.urls"))]\n'
    urls.write_text(u)
print('Configurações atualizadas. Execute: python manage.py makemigrations estacionamento && python manage.py migrate')
