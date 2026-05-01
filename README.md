# Task Manager API\

## Core Stack
- **FastAPI**: Modern, fast (high-performance) web framework.
- **SQLAlchemy**: Async database toolkit and ORM.
- **Alembic**: Database migrations tool.
- **Pydantic V2**: Data validation and settings management.
## Installation

1. **Install requirements:**
   ```bash
   pip install -r requirements.txt
   ```

## Database Migrations

### 1. Initialize Migration Environment
```bash
python -m alembic init alembic
```
make migrations
```bash
python -m alembic revision --autogenerate -m "init"
```

apply migrations
```bash
python -m alembic upgrade head
```
