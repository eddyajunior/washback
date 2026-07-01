# WashBack 🚗🧼

WashBack é uma API backend para gestão de lava-rápidos, com foco em cadastro de clientes, registro de lavagens, análise de recorrência, indicadores operacionais e suporte a campanhas de retenção.

O projeto foi desenvolvido como um MVP evolutivo utilizando boas práticas de engenharia de software, arquitetura em camadas, autenticação JWT, testes automatizados, migrations com Alembic, lint com Ruff e pipeline de CI com GitHub Actions.

## Principais funcionalidades

### Autenticação e Segurança
- Registro de usuários
- Login com JWT
- Proteção de endpoints por token
- Isolamento de dados por empresa (multi-tenant)

### Gestão de Clientes
- Cadastro de clientes
- Consulta por ID
- Atualização e exclusão
- Controle de placas duplicadas

### Gestão de Lavagens
- Registro de lavagens realizadas
- Histórico por empresa
- Paginação de resultados

### Analytics e Inteligência
- Clientes ativos
- Clientes recorrentes
- Identificação de clientes inativos
- KPIs operacionais
- Base para campanhas de retenção

### Qualidade de Engenharia
- Testes automatizados
- Coverage gate
- Lint com Ruff
- CI com GitHub Actions

## Arquitetura

O projeto segue arquitetura em camadas com princípios inspirados em Clean Architecture e Separation of Concerns.

### Fluxo de execução

```text
Client
 ↓
FastAPI Router
 ↓
Application Services
 ↓
Repositories
 ↓
Database
```

### Camadas

#### Routers
Responsáveis por expor endpoints HTTP, validar requests e delegar chamadas para a camada de serviço.

#### Services
Implementam regras de negócio, validações e casos de uso da aplicação.

#### Repositories
Responsáveis pelo acesso aos dados e abstração das operações de persistência.

#### Database
Camada de persistência baseada em SQLAlchemy ORM com versionamento de schema via Alembic.
```

## Stack Tecnológica

### Backend / API
- Python 3.14
- FastAPI
- Pydantic

### Persistência
- SQLite
- SQLAlchemy ORM
- Alembic (database migrations)

### Segurança
- JWT Authentication
- Passlib / bcrypt

### Qualidade de Código
- Pytest
- Pytest Coverage
- Ruff Linter

### CI / Versionamento
- Git
- GitHub
- GitHub Actions

## Estrutura de Pastas

```bash
app/
├── application/
│   └── services/          # Regras de negócio
│
├── core/
│   ├── middlewares/       # Logging, request tracing
│   ├── exceptions/        # Exceptions customizadas
│   └── logger/            # Configuração de logs
│
├── infrastructure/
│   ├── database/          # Engine, session, models
│   └── repositories/      # Acesso a dados
│
├── routers/               # Endpoints FastAPI
├── schemas/               # Request / Response DTOs
└── main.py                # Bootstrap da aplicação
```

## Setup Local

### 1. Clonar o repositório

```bash
git clone https://github.com/eddyajunior/washback.git
cd washback
```

### 2. Criar ambiente virtual

```bash
python -m venv .venv
```

### 3. Ativar ambiente virtual

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar dependências

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`.

### 6. Rodar migrations

```bash
alembic upgrade head
```

### 7. Executar a API

```bash
uvicorn app.main:app --reload
```

A documentação interativa estará disponível em:

```text
http://127.0.0.1:8000/docs
```

## Variáveis de Ambiente

O projeto utiliza variáveis de ambiente para configurações sensíveis e específicas de cada ambiente.

Crie um arquivo `.env` na raiz do projeto com base no arquivo `.env.example`.

```env
DATABASE_URL=sqlite:///./washback.db
SECRET_KEY=change_me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### Descrição das variáveis

| Variável | Descrição |
|---|---|
| `DATABASE_URL` | String de conexão com o banco de dados |
| `SECRET_KEY` | Chave usada para assinatura dos tokens JWT |
| `ALGORITHM` | Algoritmo usado na geração dos tokens |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Tempo de expiração do token |

## Qualidade de Código

O projeto utiliza testes automatizados, lint e pipeline de integração contínua para garantir estabilidade e qualidade do código.

### Testes

Executar todos os testes:

```bash
pytest -v
```

### Coverage

Executar testes com cobertura:

```bash
pytest --cov=app --cov-report=term-missing
```

O projeto possui coverage gate mínimo de **60%** na pipeline de CI.

### Lint

Executar análise estática:

```bash
python -m ruff check app tests
```

### CI (GitHub Actions)

A pipeline executa automaticamente em cada push ou pull request:

- Instalação de dependências
- Ruff lint
- Pytest
- Coverage gate
```

## Database Migrations

O projeto utiliza **Alembic** para versionamento e evolução controlada do schema do banco de dados.

### Criar uma migration

Após alterar models SQLAlchemy:

```bash
alembic revision --autogenerate -m "descricao_da_migration"
```

### Aplicar migrations

```bash
alembic upgrade head
```

### Reverter última migration

```bash
alembic downgrade -1
```

> Recomenda-se revisar manualmente os arquivos gerados antes de aplicar migrations em ambientes compartilhados.
```

## Roadmap

### MVP (concluído)
- [x] Autenticação JWT
- [x] Gestão de clientes
- [x] Gestão de lavagens
- [x] Analytics operacionais
- [x] Dashboard de KPIs
- [x] Testes automatizados
- [x] CI com GitHub Actions
- [x] Lint com Ruff
- [x] Database migrations com Alembic

### Próximos passos (curto prazo)
- [ ] Melhorar documentação de API
- [ ] Expandir cobertura de testes
- [ ] Melhorar health check
- [ ] Adicionar pre-commit hooks
- [ ] Refatorar AI module

### Evoluções futuras (médio/longo prazo)
- [ ] Engine de recomendação de campanhas
- [ ] Notificações automáticas via WhatsApp
- [ ] Migração para PostgreSQL
- [ ] Deploy em cloud
- [ ] Observabilidade avançada (metrics/tracing)