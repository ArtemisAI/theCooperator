# Environment Setup for the Demo

Create a `.env` file in the project root with the following values if you want to run against PostgreSQL and enable Celery. The demo and tests default to SQLite so these are optional.

```
POSTGRES_HOST=postgres
POSTGRES_DB=thecooperator
POSTGRES_USER=tc_app
POSTGRES_PASSWORD=super-secret
JWT_SECRET=change-me
CELERY_BROKER_URL=redis://redis:6379/0
```

Load the variables before starting the backend:

```bash
export $(grep -v '^#' .env | xargs)
uvicorn app.api:app --reload
```
