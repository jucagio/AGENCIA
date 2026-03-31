# Variables de Entorno — MAPER.IA (WhatsApp Business + Gemini)

Variables que n8n necesita para operar el asesor MAPER.IA por WhatsApp.

## Supabase

| Variable | Descripcion | Donde obtenerla |
|----------|-------------|-----------------|
| `SUPABASE_URL` | URL del proyecto Supabase | Dashboard > Settings > API > Project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Clave con acceso completo (bypasea RLS) | Dashboard > Settings > API > Service Role Key |

## WhatsApp Business API (Meta)

| Variable | Descripcion | Donde obtenerla |
|----------|-------------|-----------------|
| `WHATSAPP_PHONE_NUMBER_ID` | ID del numero 3107735189 en Meta | Meta Developer Portal > WhatsApp > Configuration > Phone numbers |
| `WHATSAPP_BUSINESS_ACCOUNT_ID` | WABA ID | Meta Developer Portal > WhatsApp > Configuration |
| `WHATSAPP_ACCESS_TOKEN` | System User Token permanente | Meta Business Manager > System Users > Generate Token |
| `META_VERIFY_TOKEN` | Token de verificacion del webhook (lo defines tu) | Valor definido: `maper_ia_whatsapp_mapersa_2026` |
| `META_APP_SECRET` | Secret de la app de Meta (para validar firmas) | Meta Developer Portal > App > Settings > Basic |

## Gemini (Google AI)

| Variable | Descripcion | Donde obtenerla |
|----------|-------------|-----------------|
| `GEMINI_API_KEY` | API key de Google Gemini | aistudio.google.com > API Keys |

## Ejemplo de .env

```env
# Supabase
SUPABASE_URL=https://lzhfyasnsxdacxkyhqpj.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# WhatsApp Business API (Meta)
WHATSAPP_PHONE_NUMBER_ID=123456789012345
WHATSAPP_BUSINESS_ACCOUNT_ID=987654321098765
WHATSAPP_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxx
META_VERIFY_TOKEN=maper_ia_whatsapp_mapersa_2026
META_APP_SECRET=abc123def456...

# Gemini
GEMINI_API_KEY=AIza...
```

## Notas de seguridad

- **SUPABASE_SERVICE_ROLE_KEY** tiene acceso total a la base de datos. NUNCA exponerla en frontend ni en logs.
- **WHATSAPP_ACCESS_TOKEN** si usas System User Token es permanente. Protegerlo igual que un password.
- **META_APP_SECRET** se usa para validar que los webhooks realmente vienen de Meta (verificar firma X-Hub-Signature-256).
- Rotar las claves periodicamente, especialmente si un miembro del equipo deja de tener acceso.

## Credenciales en n8n (Settings > Credentials)

| Nombre en n8n | Tipo | Datos |
|---------------|------|-------|
| `Gemini MAPERSA` | Google Gemini (PaLM) Api | API Key de Gemini |
| `Supabase MAPERSA` | Supabase | URL + Service Role Key |
| `Meta MAPERSA` | Header Auth | `Authorization: Bearer {WHATSAPP_ACCESS_TOKEN}` |
