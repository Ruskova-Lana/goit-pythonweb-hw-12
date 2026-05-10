# Contacts REST API

REST API application for contact management built with FastAPI, PostgreSQL, JWT authentication, Redis caching, Cloudinary integration, email verification, password reset, role-based access control, unit testing, integration testing, and Sphinx documentation.

---

# Features

- User registration and authentication
- JWT access tokens
- Email verification
- Password reset via email
- CRUD operations for contacts
- Contact search
- Upcoming birthdays
- Redis caching
- Role-based access (`user`, `admin`)
- Avatar upload with Cloudinary
- Rate limiting
- CORS support
- Swagger/OpenAPI documentation
- Unit and integration tests
- Docker Compose support
- Sphinx documentation

---

# Technologies

- FastAPI
- PostgreSQL
- SQLAlchemy
- Redis
- Docker Compose
- JWT (python-jose)
- Passlib / bcrypt
- Cloudinary
- FastAPI-Mail
- Pytest
- Pytest-cov
- Sphinx

---

# Project Structure

```text
GOIT-PYTHONWEB-HW-12/
│
├── docs/
│
├── goit_hw_12/
│   ├── __init__.py
│   ├── auth.py
│   ├── cloudinary_service.py
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── email_service.py
│   ├── main.py
│   ├── models.py
│   ├── redis_client.py
│   ├── schemas.py
│   └── users.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth_routes.py
│   ├── test_auth_unit.py
│   ├── test_cloudinary_service.py
│   ├── test_contacts_routes.py
│   ├── test_contacts_unit.py
│   ├── test_email_service.py
│   ├── test_extra_routes.py
│   └── test_users_routes.py
│
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── poetry.lock
├── pyproject.toml
├── pytest.ini
└── README.md
```

---

# Installation

## Clone repository

```bash
git clone https://github.com/your-username/goit-pythonweb-hw-12.git
```

```bash
cd goit-pythonweb-hw-12
```

---

# Install dependencies

```bash
poetry install
```

---

# Environment Variables

Create `.env` file based on `.env.example`.

Example:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/contacts_db

SECRET_KEY=super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

MAIL_USERNAME=example@gmail.com
MAIL_PASSWORD=your_password
MAIL_FROM=example@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com

CLOUDINARY_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret

REDIS_HOST=localhost
REDIS_PORT=6379
```

---

# Run Docker Services

```bash
docker compose up -d
```

---

# Run Application

```bash
poetry run uvicorn goit_hw_12.main:app --reload
```

Application URL:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

OpenAPI schema:

```text
http://127.0.0.1:8000/openapi.json
```

---

# Authentication

The application uses JWT access tokens.

## Signup

```http
POST /auth/signup
```

## Login

```http
POST /auth/login
```

# Email Verification Flow

1. User registers via `POST /auth/signup`.
2. The application creates a user with `confirmed = false`.
3. A verification token is generated and sent to the user's email.
4. User follows the verification link:

```text
GET /auth/confirmed_email/{token}
```

5. After successful verification, `confirmed` becomes `true`.
6. Only confirmed users can log in via `POST /auth/login`.

---

# Contacts Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /contacts/ | Get all contacts |
| GET | /contacts/{id} | Get contact by ID |
| POST | /contacts/ | Create contact |
| PUT | /contacts/{id} | Update contact |
| DELETE | /contacts/{id} | Delete contact |
| GET | /contacts/search/ | Search contacts |
| GET | /contacts/birthdays/ | Upcoming birthdays |

---

# User Features

- Email verification
- Password reset
- Avatar upload
- Redis caching
- Rate limiting
- Role-based permissions

---

# Roles

Supported roles:

- `user`
- `admin`

Only administrators can update default avatars.

---

# Redis Caching

Redis is used for caching authenticated users.

---

# Testing

The project contains:

- Unit tests
- Integration tests

Testing tools:

- pytest
- pytest-asyncio
- pytest-cov
- httpx

## Run tests

```bash
poetry run python -m pytest tests/
```

## Run tests with coverage

```bash
poetry run python -m pytest --cov=goit_hw_12 --cov-report=term-missing tests/
```

Current test coverage:

```text
75%
```

---

# Generate HTML Coverage Report

```bash
poetry run python -m pytest --cov=goit_hw_12 --cov-report=html tests/
```

Coverage report will be generated in:

```text
htmlcov/index.html
```

---

# Sphinx Documentation

Generate documentation:

```bash
sphinx-build -b html docs docs/_build
```

---

# API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI schema:

```text
http://127.0.0.1:8000/openapi.json
```

---

# Author

Ruslana Uskova