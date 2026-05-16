# Contacts REST API

REST API application for managing contacts built with FastAPI, PostgreSQL, Redis, JWT authentication, Cloudinary avatar storage, email verification, and role-based access control.

---

# Features

- User registration and login
- JWT authentication
- Email verification
- Password hashing with Passlib/Bcrypt
- Password reset via email
- Role-based access (`user` / `admin`)
- CRUD operations for contacts
- Search contacts
- Upcoming birthdays
- Cloudinary avatar upload
- Redis caching for authenticated users
- Request rate limiting
- CORS configuration
- Docker Compose support
- Unit and integration tests
- Sphinx-ready docstrings
- Test coverage > 75%

---

# Technologies

- FastAPI
- PostgreSQL
- SQLAlchemy
- Redis
- JWT / python-jose
- Passlib / bcrypt
- Cloudinary
- SlowAPI
- Pytest
- Docker Compose
- Poetry

---

# Project Structure

```text
goit-pythonweb-hw-12/
│
├── goit_hw_12/
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
├── docs/
├── htmlcov/
├── Dockerfile
├── docker-compose.yml
├── poetry.lock
├── pyproject.toml
├── pytest.ini
├── README.md
├── .env
├── .env.example
└── .gitignore
```

---

# Installation

## Clone repository

```bash
git clone https://github.com/Ruskova-Lana/goit-pythonweb-hw-12.git
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

Example for local run:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/contacts_db

SECRET_KEY=super_secret_key_change_me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_email_app_password
MAIL_FROM=your_email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com

CLOUDINARY_NAME=your_cloudinary_cloud_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret

REDIS_HOST=localhost
REDIS_PORT=6379
```

Example for Docker Compose:

```env
DATABASE_URL=postgresql://postgres:postgres123@db:5432/contacts_db

REDIS_HOST=redis
REDIS_PORT=6379
```

---

# Running with Docker Compose

## Start services

```bash
docker compose up --build
```

This starts:
- FastAPI application
- PostgreSQL
- Redis

---

# Running locally

## Start PostgreSQL and Redis

Make sure PostgreSQL and Redis are running locally.

## Run application

```bash
poetry run uvicorn goit_hw_12.main:app --reload
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

# Authentication Flow

## User registration

```http
POST /auth/signup
```

After successful registration:
- password is hashed
- verification email is sent
- user is stored in database

---

## Email verification

User receives verification link:

```http
GET /auth/confirmed_email/{token}
```

After verification:
- `confirmed=True`
- user can login

---

## Login

```http
POST /auth/login
```

Returns:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

---

## Refresh Token

```http
GET /auth/refresh_token
```
Header:
`Authorization: Bearer <your_refresh_token>`

Returns:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```

---

# Contacts Functionality

Authenticated users can:
- create contacts
- update contacts
- delete contacts
- search contacts
- view upcoming birthdays

Users only have access to their own contacts.

---

# Roles

Supported roles:
- `user`
- `admin`

Only admins can:
- update default avatar functionality

---

# Redis Caching

Authenticated users are cached in Redis.

`get_current_user()`:
- first checks Redis
- if user exists in cache → database is not queried
- otherwise user is loaded from PostgreSQL and cached

---

# Rate Limiting

Rate limiting is enabled with SlowAPI.

Example:
- `/users/me` endpoint has request limits

---

# CORS

CORS is configured for local frontend development.

Example allowed origins:

```python
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

---

# Testing

The project includes:
- unit tests
- integration tests
- authentication tests
- Redis cache tests
- role-based access tests
- CRUD business logic tests

Run tests:

```bash
poetry run pytest
```

The tests will automatically generate a coverage report (`htmlcov/` and `coverage.xml`) due to settings in `pytest.ini`.

---

# Coverage Report

HTML coverage report is generated in:

```text
htmlcov/
```

Open:

```text
htmlcov/index.html
```

in browser to inspect detailed coverage.

---

# Sphinx Documentation

Generate documentation:

```bash
sphinx-build -b html docs docs/_build
```

Generated documentation:

```text
docs/_build/index.html
```

---

# Cloud Deployment & CI/CD

This project is configured for cloud deployment:
- **Render.com**: The `render.yaml` file defines the infrastructure as code to automatically deploy the FastAPI application, PostgreSQL database, and Redis cache.
- **GitHub Actions**: The `.github/workflows/main.yml` file sets up a CI pipeline that runs tests and uploads coverage reports on every push and pull request.

---

# Security

- Passwords are hashed
- JWT authentication is used
- Secrets are stored in `.env`
- Redis cache reduces DB load
- Email verification is required
- Role-based access is enforced

---

# Author

Ruslana Uskova