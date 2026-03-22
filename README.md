# 🎬 CineReserve API

API RESTful para gerenciamento de filmes e sessões do cinema **Cinépolis Natal**, desenvolvida com Django REST Framework.

---

## 🛠️ Tecnologias

- Python 3.12
- Django 6.0 + Django REST Framework
- PostgreSQL 15
- JWT Authentication (djangorestframework-simplejwt)
- Poetry
- Docker + Docker Compose

---

## ⚙️ Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
POSTGRES_DB=cinereserve
POSTGRES_USER=postgres
POSTGRES_PASSWORD=sua_senha
POSTGRES_HOST=localhost   # use 'db' ao rodar com Docker
POSTGRES_PORT=5432

SECRET_KEY=sua_secret_key_django
DEBUG=True
```

---

## 🚀 Como rodar localmente

**Pré-requisitos:** Python 3.12, Poetry e Docker instalados.

**1. Clone o repositório**
```bash
git clone https://github.com/thiagoeduardoc/cinereserve-api.git
cd cinereserve-api
```

**2. Instale as dependências**
```bash
poetry install
```

**3. Suba o banco de dados**
```bash
docker compose up db -d
```

**4. Rode as migrations**
```bash
poetry run python manage.py migrate
```

**5. Inicie o servidor**
```bash
poetry run python manage.py runserver
```

A API estará disponível em `http://localhost:8000`.

---

## 🐳 Como rodar com Docker

Certifique-se de que o `.env` está configurado com `POSTGRES_HOST=db`.

```bash
docker compose up --build
```

A API estará disponível em `http://localhost:8000`.

Para rodar em background:
```bash
docker compose up --build -d
```

Para parar:
```bash
docker compose down
```

---

## 📖 Documentação Interativa

A API possui documentação interativa gerada automaticamente via Swagger.

Acesse após subir o projeto:
- **Swagger UI:** http://localhost:8000/api/docs/
- **Schema OpenAPI:** http://localhost:8000/api/schema/

---

## 🔗 Endpoints da API

### 🔐 Autenticação — `/api/accounts/`

#### Cadastro de usuário
```
POST /api/accounts/register/
```
Body:
```json
{
    "username": "user",
    "email": "user@email.com",
    "name": "User",
    "password": "suasenha123"
}
```

#### Login
```
POST /api/accounts/login/
```
Body:
```json
{
    "username": "user",
    "password": "suasenha123"
}
```
Resposta:
```json
{
    "access": "eyJ...",
    "refresh": "eyJ..."
}
```

#### Renovar token
```
POST /api/accounts/refresh/
```
Body:
```json
{
    "refresh": "eyJ..."
}
```

#### Dados do usuário logado
```
GET /api/accounts/me/
Authorization: Bearer {access_token}
```

---

### 🎥 Filmes — `/api/movies/`

#### Listar filmes disponíveis
```
GET /api/movies/
```
Não requer autenticação. Suporta paginação.

Resposta:
```json
{
    "count": 10,
    "next": "http://localhost:8000/api/movies/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Nome do Filme",
            "synopsis": "Sinopse do filme...",
            "genre": "action",
            "duration": 120,
            "is_active": true
        }
    ]
}
```

---

### 🎞️ Sessões — `/api/movies/{movie_id}/sessions/`

#### Listar sessões de um filme
```
GET /api/movies/{movie_id}/sessions/
```
Não requer autenticação. Suporta paginação.

Resposta:
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "movie": 1,
            "movie_title": "Nome do Filme",
            "room_name": "Sala 1",
            "start_time": "2025-01-20T19:00:00Z",
            "end_time": "2025-01-20T21:00:00Z",
            "room_capacity": 100
        }
    ]
}
```

---

### 💺 Assentos — `/api/movies/sessions/{session_id}/seats/`

#### Mapa de assentos de uma sessão
```
GET /api/movies/sessions/{session_id}/seats/
```
Não requer autenticação. Retorna todos os assentos com seus status.

Resposta:
```json
{
    "count": 100,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "row": "A",
            "number": 1,
            "status": "available"
        },
        {
            "id": 2,
            "row": "A",
            "number": 2,
            "status": "purchased"
        }
    ]
}
```

Status possíveis: `available`, `reserved`, `purchased`.

---

### 🎟️ Reserva — `/api/movies/sessions/{session_id}/seats/{seat_id}/reserve/`

#### Reservar um assento
```
POST /api/movies/sessions/{session_id}/seats/{seat_id}/reserve/
Authorization: Bearer {access_token}
```
Não requer body. Requer autenticação.

Resposta:
```json
{
    "id": 1,
    "seat": {
        "id": 1,
        "row": "A",
        "number": 1,
        "status": "purchased"
    },
    "session": {
        "id": 4,
        "movie": "Nome do Filme",
        "room": "Sala 1",
        "start_time": "2025-01-20T19:00:00Z"
    },
    "purchased_at": "2025-01-20T18:00:00Z"
}
```

---

### 🗂️ Meus Tickets — `/api/movies/my-tickets/`

#### Listar tickets do usuário logado
```
GET /api/movies/my-tickets/
Authorization: Bearer {access_token}
```
Suporta paginação.

Resposta:
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "seat": {
                "id": 1,
                "row": "A",
                "number": 1,
                "status": "purchased"
            },
            "session": {
                "id": 4,
                "movie": "Nome do Filme",
                "room": "Sala 1",
                "start_time": "2025-01-20T19:00:00Z"
            },
            "purchased_at": "2025-01-20T18:00:00Z"
        }
    ]
}
```

---

## 📁 Estrutura do Projeto

```
cinereserve-api/
├── accounts/          # Usuários e autenticação
├── core/              # Configurações do projeto
├── movies/            # Filmes
├── movie_sessions/    # Sessões, assentos e tickets
├── tests/             # Testes
├── .env               # Variáveis de ambiente (não versionado)
├── docker-compose.yml
├── Dockerfile
└── manage.py
```