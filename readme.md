# 📚 4000 Essential English Words API

A production-ready REST API that provides access to **4000 essential English vocabulary words**, built with **FastAPI, PostgreSQL, SQLAlchemy, Alembic, and JWT Authentication**.

Designed with clean architecture and scalable backend practices, this project demonstrates how to build a real-world API with authentication, database management, and structured code organization.

---

## Live API: http://ec2-15-185-205-177.me-south-1.compute.amazonaws.com:8003/

## 🚀 Features

- 🔐 JWT Authentication (Register / Login)
- 📖 4000 Essential English Vocabulary dataset
- 🔎 Retrieve words with clean API endpoints
- 🧱 Modular & scalable project structure
- 🐘 PostgreSQL database integration
- ⚙️ SQLAlchemy ORM for database operations
- 🔄 Alembic migrations for version control
- 📑 Auto-generated API docs (Swagger UI)

---

## 🏗️ Tech Stack

- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Authentication:** JWT (JSON Web Tokens)

---

## 📂 Project Structure

```
app/
├── api/            # API routes
├── core/           # Config & security
├── models/         # Database models
├── schemas/        # Pydantic schemas
├── services/       # Business logic
├── db/             # Database connection
└── main.py         # Entry point
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```
git clone https://github.com/aladdinshammr/fastapi-4000-Essential-English-Words.git
cd fastapi-4000-Essential-English-Words
```

### 2. Create virtual environment

```
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```
export DATABASE_HOST=localhost
export DATABASE_PORT=5432
export DATABASE_NAME=database_name
export DATABASE_USER=user
export DATABASE_PASSWORD=password
export BASE_URL=http://localhost:8000
export SECRET_KEY=your_secret_key
export ALGORITHM=HS256
export ACCESS_TOKEN_EXPIRE_MINUTES=3000
```

---

### 5. Run migrations

```
alembic upgrade head
```

---

### 6. Run the server

```
uvicorn app.main:app --reload
```

---

## 📖 API Documentation

Once the server is running, access:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 🔐 Authentication

### Register

```
POST /auth/register
```

### Login

```
POST /auth/login
```

Response:

```json
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```

---

## 📚 Example Endpoints

| Method | Endpoint       | Description              |
| ------ | -------------- | ------------------------ |
| GET    | /words         | Get all vocabulary words |
| GET    | /words/{id}    | Get word by ID           |
| POST   | /auth/login    | Login user               |
| POST   | /auth/register | Register user            |

---

## 🧪 Example Response

```json
{
  "word": "abandon",
  "meaning": "to leave completely",
  "example": "He abandoned the car."
}
```

---

## 🧩 Future Improvements

- 🚀 Add pagination & filtering
- 🔍 Full-text search
- ⚡ Redis caching
- 🐳 Docker support
- 🌍 Deploy to cloud (AWS / Render / Railway)
- 🧪 Add unit & integration tests

---

## 👤 Author

**Aladdin Shammr**

- GitHub: [https://github.com/aladdinshammr](https://github.com/aladdinshammr)

---

## 📄 License

This project is licensed under the MIT License.

---

## ⭐ Why This Project?

This project demonstrates:

- Building a real-world REST API with FastAPI
- Implementing secure authentication using JWT
- Managing database schema with Alembic
- Writing clean, maintainable backend code

---

⭐ If you found this project useful, consider giving it a star!

---
