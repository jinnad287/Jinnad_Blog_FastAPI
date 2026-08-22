# Blog API (FastAPI)

A robust, production-ready RESTful Blog API built with **FastAPI**, **SQLAlchemy**, and **Pydantic**. It features secure user authentication with JWT, role-based resource management, custom exception handling, structured request logging middleware, and SQLite/PostgreSQL database compatibility.

---

## Features

- **User Authentication:** Secure registration and login leveraging password hashing (`Passlib`) and JWT token creation.
- **Blog Management:** Full CRUD operations (Create, Read, Update, Delete) for blog posts.
- **Resource Authorization:** Strict ownership checks ensuring users can only edit or delete their own authored blogs.
- **Custom Exception Handling:** Centralized custom exception classes and handlers returning clean, structured error responses.
- **Request Logging Middleware:** Detailed request tracking logging HTTP methods, endpoints, response statuses, and execution durations to the `logs/` directory.
- **Database Architecture:** Built with SQLAlchemy ORM, using a local SQLite file (`blog.db`) for development.

---

## Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Data Validation:** [Pydantic](https://docs.pydantic.dev/) & `pydantic-settings`
- **Server:** [Uvicorn](https://www.uvicorn.org/)
- **Security:** `python-jose` (JWT), `passlib`
- **Database:** SQLite (`blog.db`)

---

## Detailed Project File Structure

```text
Jinnad_Blog_FastAPI/
│
├── app/                  # Main application package
│   ├── api/              # API route handlers and endpoints
│   ├── core/             # Core configurations, security, and dependencies
│   ├── database/         # Database session management and base setup
│   ├── models/           # SQLAlchemy ORM models (Database tables)
│   ├── schemas/          # Pydantic data schemas for validation and serialization
│   └── main.py           # Application entry point, middleware, and exception handlers
│
├── logs/                 # Directory containing application execution and access logs
├── .env                  # Local environment variables configuration file
├── README.md             # Project documentation
├── blog.db               # Local SQLite database file
└── requirements.txt      # Python dependencies list
