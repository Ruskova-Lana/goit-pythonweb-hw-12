# Contacts REST API

REST API application built with FastAPI for managing contacts with JWT authentication, email verification, rate limiting, CORS support, and avatar upload via Cloudinary.

## Features

* User registration and login
* JWT authentication (`access_token`)
* Email verification
* Password hashing with bcrypt
* CRUD operations for contacts
* Search contacts by first name, last name, or email
* Upcoming birthdays endpoint
* Access only to own contacts
* Rate limiting for `/users/me`
* CORS support
* Avatar upload with Cloudinary
* PostgreSQL database
* Docker Compose support
* Swagger documentation

---

# Technologies

* FastAPI
* SQLAlchemy
* PostgreSQL
* Poetry
* JWT (python-jose)
* Passlib / bcrypt
* FastAPI-Mail
* Cloudinary
* Docker Compose

---

# Project Structure

```text
GOIT-PYTHONWEB-HW-10/
│
├── goit_hw_10/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── auth.py
│   ├── users.py
│   ├── config.py
│   ├── email_service.py
│   └── cloudinary_service.py
│
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yml
├── poetry.lock
├── pyproject.toml
└── README.md
```

---

# Installation

## 1. Clone repository

```bash
git clone https://github.com/Ruskova-Lana/goit-pythonweb-hw-10.git
cd goit-pythonweb-hw-10
```

---

## 2. Install dependencies

```bash
poetry install --no-root
```

---

## 3. Configure environment variables

Create `.env` file based on `.env.example`

Example:

```env
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/contacts_db

SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_FROM=your_email@gmail.com
MAIL_PORT=587
MAIL_SERVER=smtp.gmail.com

CLOUDINARY_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
```

---

# Run PostgreSQL with Docker

```bash
docker compose up -d
```

---

# Run application

```bash
poetry run uvicorn goit_hw_10.main:app --reload
```

Application will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Authentication

## Register user

`POST /auth/signup`

Example request:

```json
{
  "username": "Ruslana",
  "email": "ruslana@test.com",
  "password": "12345678"
}
```

---

## Login

`POST /auth/login`

Use:

```text
username = email
password = user password
```

Successful response:

```json
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
```

---

## Swagger Authorization

Click `Authorize` in Swagger UI and insert token:

```text
Bearer your_access_token
```

---

# Contacts Endpoints

| Method | Endpoint               | Description        |
| ------ | ---------------------- | ------------------ |
| POST   | `/contacts/`           | Create contact     |
| GET    | `/contacts/`           | Get all contacts   |
| GET    | `/contacts/{id}`       | Get contact by ID  |
| PUT    | `/contacts/{id}`       | Update contact     |
| DELETE | `/contacts/{id}`       | Delete contact     |
| GET    | `/contacts/search/`    | Search contacts    |
| GET    | `/contacts/birthdays/` | Upcoming birthdays |

---

# User Endpoints

| Method | Endpoint        | Description          |
| ------ | --------------- | -------------------- |
| GET    | `/users/me`     | Current user profile |
| PATCH  | `/users/avatar` | Upload avatar        |

---

# Email Verification

After registration user receives verification email.

Verification endpoint:

```text
GET /auth/confirmed_email/{token}
```

---

# Rate Limiting

Endpoint:

```text
/users/me
```

is limited to:

```text
5 requests per minute
```

---

# CORS

CORS middleware is enabled for the application.

---

# Password Security

Passwords are hashed using bcrypt before saving to database.

---

# Docker Compose

Application uses Docker Compose for PostgreSQL database.

Run:

```bash
docker compose up -d
```

Stop:

```bash
docker compose down
```

---

# Author

Ruslana Uskova
