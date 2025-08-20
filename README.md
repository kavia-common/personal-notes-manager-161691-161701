# personal-notes-manager-161691-161701

Notes Backend (Flask)
- Entrypoint: notes_backend/run.py (main)
- Default bind: 0.0.0.0:3001
- Healthcheck: GET /
- API docs (Swagger UI via flask-smorest): /docs

Environment variables
See notes_backend/.env.example for commonly used variables:
- HOST (default 0.0.0.0)
- PORT (default 3001)
- FLASK_DEBUG (0 or 1)
- LOG_LEVEL
- FLASK_SECRET_KEY, JWT_SECRET_KEY
- JWT_ACCESS_TOKEN_EXPIRES
- CORS_ORIGINS
- NOTES_DATABASE_URL or DATABASE_URL

Local run
- Install dependencies: pip install -r notes_backend/requirements.txt
- Run: python notes_backend/run.py
- Visit: http://localhost:3001/