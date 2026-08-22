# Blog API (FastAPI)

A robust, production-ready RESTful Blog API built with **FastAPI**, **SQLAlchemy**, and **Pydantic**. It features secure user authentication, role-based resource management, custom exception handling, and structured request logging.

---

## Features

- **User Authentication:** Secure user registration and login using JWT tokens and password hashing (`Passlib` with Argon2).
- **Blog Management:** Full CRUD operations (Create, Read, Update, Delete) for blog posts.
- **Authorization:** Resource ownership validation ensuring users can only modify or delete their own posts.
- **Advanced Routing & Validation:** Powered by Pydantic v2 data validation and dynamic slug generation for blog URLs.
- **Middleware & Logging:** Custom request logging middleware tracking HTTP methods, URLs, response statuses, and execution duration.
- **Error Handling:** Centralized custom exception handlers providing clean, descriptive error responses.

---

## Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Data Validation:** [Pydantic](https://docs.pydantic.dev/)
- **Server:** [Uvicorn](https://www.uvicorn.org/)
- **Database:** SQLite (Default / Local dev)

---

## Project Structure

```text
Blog-API(FastAPI)/
│
├── app/
│   ├── api/          # Route handlers (users, blogs)
│   ├── core/         # Security, database configuration, settings
│   ├── models/       # SQLAlchemy database models
│   ├── schemas/      # Pydantic request/response schemas
│   └── main.py       # FastAPI application entry point & middleware
│
├── venv/             # Python virtual environment
├── requirements.txt  # Project dependencies
└── README.md         # Project documentation