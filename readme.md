# Enterprise Subscription Engine

![Coverage](https://img.shields.io/badge/Coverage-90%25-brightgreen)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![React](https://img.shields.io/badge/Frontend-React-61DAFB)
![Redux](https://img.shields.io/badge/State-Redux--Toolkit-764ABC)

A production-grade, full-stack subscription management system built with **FastAPI** and **React**. This project serves as a blueprint for high-reliability software, featuring rigorous automated testing, secure authentication, and a scalable architecture.

---

## System Architecture

The application follows a decoupled architecture, ensuring separation of concerns between the high-performance Python backend and the modern React frontend.



### Core Components:
* **API Layer:** FastAPI with asynchronous request handling.
* **Data Layer:** PostgreSQL managed via SQLAlchemy ORM.
* **State Management:** Centralized global state via Redux Toolkit.
* **Background Tasks:** Redis & Celery for asynchronous processing (e.g., subscription expiry).

---

## Key Features

### Security & Authentication
* **OAuth2 with JWT:** Secure token-based authentication.
* **RBAC (Role-Based Access Control):** Granular permissions for Admins and Standard Users.
* **Ownership Verification:** Strict logic preventing users from accessing or modifying unauthorized data.

### Subscription Management
* **Plan Lifecycles:** Automated start/end date calculations using `relativedelta`.
* **Concurrency Control:** Logic to prevent duplicate active subscriptions.
* **Admin Dashboard:** Full CRUD capabilities for managing service plans and monitoring user activity.

### Quality Assurance
* **90% Test Coverage:** Achieving industry-standard reliability through `pytest`.
* **Integration Testing:** End-to-end testing of the API flow using `FastAPI TestClient`.

---

## Tech Stack

| Category | Technology |
| :--- | :--- |
| **Backend** | Python, FastAPI, SQLAlchemy, PostgreSQL, Pydantic |
| **Frontend** | React (Vite), Redux Toolkit, Axios, Tailwind CSS |
| **Testing** | Pytest, Coverage.py |
| **Infrastructure** | Docker, Redis, Celery |

---

## Testing & Coverage

Testing is not an afterthought in this project; it is the foundation. We utilize `coverage.py` to ensure every critical path is validated.

```bash
# Run tests and generate coverage report
pytest --cov=app tests/ --cov-report=term-missing

Installation & Setup
Backend
cd subscription_backend

python -m venv venv

source venv/bin/activate # On Windows: venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload

Frontend
cd subscription_frontend

npm install

npm run dev

Roadmap
[ ] Stripe Integration: Seamless payment gateway connection.

[ ] Agentic RAG Analytics: AI-driven insights for subscription churn and usage.

[ ] Dockerization: Containerizing the entire stack for one-click deployment.