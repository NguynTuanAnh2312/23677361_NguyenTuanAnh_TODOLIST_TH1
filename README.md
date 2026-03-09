# ToDo List API (FastAPI)

## Requirements
- Python 3.12+
- (Windows) PowerShell recommended

## Setup
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Run migrations
```bash
alembic upgrade head
```

## Run server
```bash
python -m uvicorn app.main:app --reload
```

Open Swagger: `http://127.0.0.1:8000/docs`

## Authentication (Level 5+)
1. Register: `POST /api/v1/auth/register`
2. Login: `POST /api/v1/auth/login` (form: username/password)
3. Click **Authorize** in Swagger and paste: `Bearer <access_token>`

## Testing (Level 7)
```bash
pytest -q
```

## Docker
See `Dockerfile` (SQLite local file is used).