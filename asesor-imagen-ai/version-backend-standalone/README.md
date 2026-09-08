# Asesor Imagen AI — Backend Standalone

**Asesor Imagen AI (Backend Standalone)** — versión aislada del backend FastAPI que analiza el cuerpo y genera recomendaciones de vestuario con IA.

## Stack

- **Backend**: FastAPI + Python 3.14
- **Database**: Supabase (PostgreSQL + Auth + Realtime)
- **Frontend**: React/Flutter (TBD)
- **ML**: Replicate (imagen) + Gemini Vision (análisis)
- **Deploy**: Railway + GitHub Actions

## Setup Local

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` → `.env.local` y completa credenciales.

```bash
python backend/app/main.py
```

## Branches

- `main` — producción
- `develop` — staging

## Team

- Sasha (Backend)
- Brook (Frontend + BD)
- Erik (Diseño)
- Cinthya (Automatización)
- Jarvis (Dirección)

