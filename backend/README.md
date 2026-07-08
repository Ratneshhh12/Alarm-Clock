# Intelligent Cognitive Alarm Platform - Backend (Milestone 1)

This repository contains **Milestone 1** of the Intelligent Cognitive Alarm Platform backend, implementing a modular, production-ready backend that includes project setup, a PostgreSQL database connection (via SQLAlchemy AsyncSession), Alembic migrations, custom User Roles, and JWT-based authentication.

---

## Technical Stack
- **Python 3.12+**
- **FastAPI** (Web framework)
- **Uvicorn** (ASGI server)
- **PostgreSQL** (Database)
- **SQLAlchemy ORM** (Database ORM using AsyncSession)
- **Alembic** (Database migration framework)
- **JWT (python-jose)** & **Bcrypt (passlib)** (Authentication & security)
- **Pydantic v2** (Request/response validation schemas)
- **Docker & Docker Compose** (Containerization setup)

---

## Directory Structure
```
backend/
├── app/
│   ├── main.py          # FastAPI app entrypoint & exception handlers
│   ├── database.py      # SQLAlchemy connection & session configuration
│   ├── config.py        # Settings configuration via Pydantic
│   ├── models.py        # SQLAlchemy database models (User & Roles enum)
│   ├── schemas.py       # Pydantic schemas (Request/Response validation)
│   ├── security.py      # JWT token generation (Access & Refresh) and hashing
│   ├── dependencies.py  # Shared dependencies (db session, active user check)
│   └── routers/
│       ├── auth.py      # Register, Login, & Logout routes
│       └── users.py     # User profile routes (protected)
├── alembic/             # Alembic migration scripts
├── requirements.txt     # Python packages list
├── .env                 # Environment variables configuration
├── .env.example         # Template for environment variables
├── Dockerfile           # Containerization configuration
├── docker-compose.yml   # Multi-container orchestrator (PostgreSQL & FastAPI)
└── README.md            # Documentation
```

---

## Setup & Running Instructions

### Option 1: Running with Docker (Recommended)
Docker Compose will automatically spin up PostgreSQL, run the Alembic database migrations, and launch the FastAPI server.

1. Make sure Docker is running on your machine.
2. Run:
   ```bash
   docker compose up --build
   ```
3. The API will be available at `http://127.0.0.1:8000`.

---

### Option 2: Running Locally (Without Docker)

#### 1. Create a Python Virtual Environment
Navigate to the `backend/` directory and create/activate a virtual environment:

**On Windows:**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Start PostgreSQL Database
Make sure PostgreSQL is running locally. Update your `.env` file with the correct credentials.

#### 4. Run Migrations
Run the Alembic migrations to create the database schemas:
```bash
alembic upgrade head
```

#### 5. Start the FastAPI Server
```bash
uvicorn app.main:app --reload
```
The server will start at `http://127.0.0.1:8000`.

---

## Environment Variables Configuration

Make a copy of `.env.example` as `.env` and fill in the details:
- `DATABASE_URL`: Connection string for PostgreSQL (supports `postgresql+asyncpg` for async access).
- `JWT_SECRET_KEY`: A cryptographically secure random string used to sign tokens.
- `JWT_ALGORITHM`: Signature hashing algorithm (default `HS256`).
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Expiration time for generated Access tokens.

---

## API Endpoints & Request/Response Examples

Access the interactive API docs at **`http://127.0.0.1:8000/docs`** (Swagger UI).

### 1. User Registration
* **Endpoint:** `POST /auth/register`
* **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "strong_password123",
    "full_name": "John Doe",
    "role": "USER" // Roles: USER, ADMIN, WELLNESS_COACH
  }
  ```
* **Success Response (201 Created):**
  ```json
  {
    "id": "e2a967f6-6cbe-4171-aa34-b2585f9be33a",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "USER",
    "is_active": true,
    "created_at": "2026-07-08T13:20:00Z",
    "updated_at": "2026-07-08T13:20:00Z"
  }
  ```

### 2. User Login (Obtain Tokens)
* **Endpoint:** `POST /auth/login`
* **Request Body (OAuth2 Form Data):**
  - `username`: `user@example.com`
  - `password`: `strong_password123`
* **Success Response (200 OK):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "token_type": "bearer"
  }
  ```

### 3. Fetch Current User Profile
* **Endpoint:** `GET /users/me`
* **Headers:** `Authorization: Bearer <access_token>`
* **Success Response (200 OK):**
  ```json
  {
    "id": "e2a967f6-6cbe-4171-aa34-b2585f9be33a",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "USER",
    "is_active": true,
    "created_at": "2026-07-08T13:20:00Z",
    "updated_at": "2026-07-08T13:20:00Z"
  }
  ```

### 4. Logout
* **Endpoint:** `POST /auth/logout`
* **Success Response (200 OK):**
  ```json
  {
    "message": "Logged out successfully"
  }
  ```

---

## Alembic Migration Commands

- **Generate a new migration script (autodetecting changes):**
  ```bash
  alembic revision --autogenerate -m "description_of_changes"
  ```
- **Apply migrations to head:**
  ```bash
  alembic upgrade head
  ```
- **Rollback last migration:**
  ```bash
  alembic downgrade -1
  ```
