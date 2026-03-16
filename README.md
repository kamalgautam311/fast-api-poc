# User Management API

FastAPI backend with user sign-up, login, and logout using PostgreSQL and JWT authentication.

## Setup

### 1. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure PostgreSQL

Create a database:

```sql
CREATE DATABASE user_management_db;
```

### 4. Environment variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env`:

```
DATABASE_URL=postgresql://user:password@localhost:5432/user_management_db
SECRET_KEY=your-secret-key  # Generate with: openssl rand -hex 32
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run the server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs

## Docker

Run the app and PostgreSQL with Docker Compose:

```bash
docker compose up --build
```

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432 (user: postgres, password: postgres)

Set a custom `SECRET_KEY` for production:

```bash
SECRET_KEY=your-secret-key docker compose up --build
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/signup` | Register a new user |
| POST | `/auth/login` | Login and get JWT token |
| POST | `/auth/logout` | Logout (revoke token) |

### Sign-up

```json
POST /auth/signup
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123"
}
```

### Login

```json
POST /auth/login
{
  "username": "johndoe",
  "password": "securepassword123"
}

Response:
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Logout

```
POST /auth/logout
Authorization: Bearer <your_access_token>
```

## Project Structure

```
app/
├── main.py           # FastAPI app
├── config.py         # Settings
├── database.py       # SQLAlchemy setup
├── dependencies.py   # Auth dependencies
├── models/
│   └── user.py       # User, TokenBlacklist models
├── routers/
│   └── auth.py       # Auth routes
├── schemas/
│   └── user.py       # Pydantic schemas
└── utils/
    └── auth.py       # Password hashing, JWT
```
