# cultiva-certificados
Sistema para geração de certificados dos cursos do Instituto Cultiva

### Como rodar o projeto
* Clone esse repositório.
* Crie um virtualenv com Python 3.
* Ative o virtualenv.
* Instale as dependências.
* Rode as migrações.

```
git https://github.com/tiagocordeiro/cultiva-certificados.git
cd cultiva-certificados
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python contrib/env_gen.py
python manage.py migrate
```

### Configurar administrador
Para cria um usuário administrador
```
python manage.py createsuperuser --username dev --email dev@foo.bar
```

### Rodar em ambiente de desenvolvimento
Para rodar o projeto localmente
```
python manage.py runserver
```

### Testes, contribuição e dependências de desenvolvimento
Para instalar as dependências de desenvolvimento
```
pip install -r requirements-dev.txt
```

Para rodar os testes
```
python manage.py test -v 2
```

Para rodar os testes com relatório de cobertura.
```
coverage run manage.py test -v 2
coverage html
```

Verificando o `Code style`
```
pycodestyle .
flake8 .
```