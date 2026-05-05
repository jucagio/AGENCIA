# Asesor de Imagen AI

Virtual Try-On & Wardrobe Assistant with AI Recommendations

**Status:** 🔨 Sprint 0 (Infrastructure)

## Project Overview

- **MVP Duration:** 14 weeks
- **Team:** Sasha (Backend), Brook (Frontend), Erik (Design)
- **Launch Target:** Week 14 (50K users)
- **Financials:** $24K/month profit @ 50K users

## Stack

| Layer | Tech | Version |
|-------|------|---------|
| Backend | FastAPI | 0.104+ |
| Database | Supabase/PostgreSQL | Latest |
| Frontend | Flutter | 3.41+ |
| Auth | JWT HS256 | - |
| Vision | Google Vision API | - |
| Try-On | Replicate | - |
| Recommendations | Claude (Anthropic) | - |
| Payments | Stripe + Mercado Pago | - |
| Infra | Railway + Supabase | - |

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Fill with credentials
uvicorn app.main:app --reload
```

### Database

Credentials needed:
- Supabase URL
- Supabase Key
- Google Vision API (JSON)
- Replicate API token
- Anthropic API key
- Stripe keys (test)
- Mercado Pago token

## Sprint 0 Checklist

- [ ] Week 1: Infrastructure (Sasha)
  - [ ] Supabase schema + RLS
  - [ ] FastAPI scaffold
  - [ ] Docker + Railway
  - [ ] CI/CD pipeline

## Documentation

- `ASESOR_IMAGEN_AI_RESUMEN_EJECUTIVO.md` - Overview & viability
- `ASESOR_IMAGEN_AI_ARQUITECTURA.md` - Technical architecture
- `ASESOR_IMAGEN_AI_SCHEMAS_Y_SERVICIOS.md` - Code templates
- `ASESOR_IMAGEN_AI_CHECKLIST_EJECUCION.md` - Execution plan

## Team

- **Sasha** - Backend/Security (FastAPI, PostgreSQL, APIs)
- **Brook** - Frontend (Flutter, Dart)
- **Erik** - Design (UI/UX, Figma)
- **Jarvis** - Architecture & Ops

## License

Internal - Agencia de Agentes Claude
