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
            "room": 1,
            "room_name": "Sala 1",
            "start_time": "2025-01-20T19:00:00Z",
            "end_time": "2025-01-20T21:00:00Z"
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
Não requer autenticação. Retorna todos os assentos da sala da sessão e a disponibilidade na sessão.

Resposta:
```json
{
    "count": 50,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "row": "A",
            "seat_number": 1,
            "is_available": true,
            "status": "available"
        },
        {
            "id": 2,
            "row": "A",
            "seat_number": 2,
            "is_available": true,
            "status": "purchased"
        }
    ]
}
```

Status possíveis: `available`, `reserved` (lock 10min), `purchased`, `unavailable`.

---

### 🔒 Reserva — `/api/movies/sessions/{session_id}/seats/{seat_id}/reserve/`

#### Reservar um assento (Lock 10 minutos)
```
POST /api/movies/sessions/{session_id}/seats/{seat_id}/reserve/
Authorization: Bearer {access_token}
```
Cria um lock temporário de **10 minutos** no assento. Requer autenticação.

Resposta:
```json
{
    "id": 1,
    "seat_row": "A",
    "seat_number": 1,
    "movie_title": "Nome do Filme",
    "room_name": "Sala 1",
    "reserved_at": "2025-01-20T18:00:00Z",
    "expires_at": "2025-01-20T18:10:00Z",
    "time_remaining": 600
}
```

⏰ **Comportamento:**
- O assento fica reservado (temporariamente bloqueado) por 10 minutos
- Outros usuários verão o status como `reserved`
- Se não comprar dentro de 10 minutos, a reserva expira e o assento fica disponível novamente
- Fazer outra reserva no mesmo assento antes de expirar retorna erro

---

### 💳 Compra — `/api/movies/sessions/{session_id}/seats/{seat_id}/purchase/`

#### Finalizar compra (Converter Reserva em Ticket)
```
POST /api/movies/sessions/{session_id}/seats/{seat_id}/purchase/
Authorization: Bearer {access_token}
```
Converte a reserva temporária em um ticket permanente. Requer reserva ativa. Requer autenticação.

Resposta:
```json
{
    "id": 1,
    "seat": {
        "id": 1,
        "row": "A",
        "seat_number": 1,
        "is_available": true,
        "status": "purchased"
    },
    "session": {
        "id": 4,
        "movie": "Nome do Filme",
        "room": "Sala 1",
        "start_time": "2025-01-20T19:00:00Z"
    },
    "purchased_at": "2025-01-20T18:05:00Z"
}
```

**Erros possíveis:**
- `Nenhuma reserva ativa encontrada` - Fazer reserva antes de comprar
- `Reserva expirada` - Timeout de 10 minutos excedido
- `Assento foi vendido para outro usuário` - Outro usuário comprou más rápido (reserva é cancelada)

---

### 📋 Minhas Reservas — `/api/movies/my-reservations/`

#### Listar reservas ativas (não expiradas)
```
GET /api/movies/my-reservations/
Authorization: Bearer {access_token}
```
Retorna apenas reservas válidas (que ainda não expiraram). Requer autenticação. Suporta paginação.

Resposta:
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "seat_row": "A",
            "seat_number": 5,
            "movie_title": "Filme X",
            "room_name": "Sala 1",
            "reserved_at": "2025-01-20T18:00:00Z",
            "expires_at": "2025-01-20T18:10:00Z",
            "time_remaining": 120
        }
    ]
}
```

---

### 🎟️ Meus Tickets — `/api/movies/my-tickets/`

#### Listar tickets comprados (permanentes)
```
GET /api/movies/my-tickets/
Authorization: Bearer {access_token}
```
Retorna todos os tickets já comprados (não expiram). Requer autenticação. Suporta paginação.

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
                "seat_number": 5,
                "is_available": true,
                "status": "purchased"
            },
            "session": {
                "id": 4,
                "movie": "Nome do Filme",
                "room": "Sala 1",
                "start_time": "2025-01-20T19:00:00Z"
            },
            "purchased_at": "2025-01-20T18:05:00Z"
        }
    ]
}
```

---

## 📁 Estrutura do Projeto

```
cinereserve-api/
├── accounts/          # Usuários e autenticação (User)
├── core/              # Configurações do projeto
├── movies/            # Filmes (Movie)
├── room/              # Salas e assentos (Room, Seat)
├── movie_sessions/    # Sessões, reservas e tickets (Session, Reservation, Ticket)
├── tests/             # Testes
├── .env               # Variáveis de ambiente (não versionado)
├── docker-compose.yml
├── dockerfile
├── manage.py
├── pyproject.toml
└── README.md
```

---

## 🏗️ Arquitetura de Dados

```
User (accounts.User)
├── has many Reservations
└── has many Tickets

Movie (movies.Movie)
└── has many Sessions

Room (room.Room)
├── has many Seats
└── has many Sessions

Seat (room.Seat)
├── has many Reservations
└── has one Ticket (OneToOneField)

Session (movie_sessions.Session)
├── FK: Movie
├── FK: Room
├── has many Reservations (lock 10min)
└── has many Tickets (permanentes)

Reservation (movie_sessions.Reservation)
├── FK: User
├── FK: Seat
├── FK: Session
└── expires_at (expiração automática em 10min)

Ticket (movie_sessions.Ticket)
├── FK: User
├── OneToOne: Seat
└── FK: Session
```

---

## ⏰ Fluxo de Reserva (CASE 5)

```
1. [GET] /api/movies/{movie_id}/sessions/
   └─ Listar sessões disponíveis

2. [GET] /api/movies/sessions/{session_id}/seats/
   └─ Ver mapa de assentos (status: available, reserved, purchased, unavailable)

3. [POST] /api/movies/sessions/{session_id}/seats/{seat_id}/reserve/
   └─ ⏱️ CRIA LOCK DE 10 MINUTOS (Reservation)
   └─ Status do assento muda para: "reserved"

4. [POST] /api/movies/sessions/{session_id}/seats/{seat_id}/purchase/
   └─ ✅ FINALIZA COMPRA (Converte Reservation → Ticket)
   └─ Status do assento muda para: "purchased"
   └─ Reservation é deletada automaticamente

Timeout automático:
- Se não comprar dentro de 10min → Reservation expira automaticamente
- APScheduler limpa Reservations expiradas a cada 1 minuto
- Assento volta a: "available"
```