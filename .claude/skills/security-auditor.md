---
name: security-auditor
description: >
  Auditoría de seguridad de código: OWASP Top 10, DevSecOps, revisión de vulnerabilidades
  en APIs, autenticación, datos y dependencias. Usar cuando se revise código antes de
  deploy a producción, cuando se necesite un code review enfocado en seguridad, o cuando
  se sospeche de vulnerabilidades. Agentes principales: Sasha, Ego.
---

# Security Auditor — Code Review de Seguridad

## OWASP Top 10 — Checklist de Auditoría

### A01 — Broken Access Control 🔴 CRÍTICO

```python
# ❌ VULNERABLE — usuario puede ver datos de otros
@app.get("/users/{user_id}/orders")
async def get_orders(user_id: str, current_user = Depends(get_current_user)):
    return await db.get_orders(user_id)  # no verifica ownership

# ✅ SEGURO — verifica que el usuario solo accede a sus propios datos
@app.get("/users/{user_id}/orders")
async def get_orders(user_id: str, current_user = Depends(get_current_user)):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(403, "Forbidden")
    return await db.get_orders(user_id)
```

**Checklist A01:**
```
[ ] Cada endpoint verifica autorización (no solo autenticación)
[ ] Usuarios no pueden acceder a recursos de otros usuarios
[ ] Principio de mínimo privilegio: roles y permisos granulares
[ ] Las acciones admin están protegidas por rol admin
[ ] IDs en URLs no son predecibles (usar UUIDs)
[ ] Logs de intentos de acceso denegados
```

---

### A02 — Cryptographic Failures 🔴 CRÍTICO

```python
# ❌ VULNERABLE
user.password = password  # texto plano
user.password = md5(password)  # MD5 es inseguro

# ✅ SEGURO
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# ❌ VULNERABLE — secreto hardcodeado
SECRET_KEY = "my-secret-key-123"

# ✅ SEGURO — desde variables de entorno
SECRET_KEY = os.environ["SECRET_KEY"]  # nunca hardcodear
```

**Checklist A02:**
```
[ ] Contraseñas con bcrypt/argon2 (nunca MD5/SHA1 para passwords)
[ ] HTTPS obligatorio en producción (HTTP rechazado)
[ ] Datos sensibles encriptados en reposo (PII, tokens)
[ ] Secretos en variables de entorno, nunca en código
[ ] .env en .gitignore — verificar git history
[ ] Tokens JWT con expiración corta (max 15 min para access tokens)
```

---

### A03 — Injection (SQL, NoSQL, Command) 🔴 CRÍTICO

```python
# ❌ SQL INJECTION
query = f"SELECT * FROM users WHERE email = '{email}'"

# ✅ SEGURO — queries parametrizadas
query = "SELECT * FROM users WHERE email = $1"
result = await db.fetchrow(query, email)

# ✅ ORM (primera línea de defensa)
user = await User.query.filter_by(email=email).first()

# ❌ COMMAND INJECTION
os.system(f"convert {filename} output.png")

# ✅ SEGURO
subprocess.run(["convert", filename, "output.png"], capture_output=True)
```

**Checklist A03:**
```
[ ] CERO concatenación de strings con input de usuario en queries
[ ] Usar ORM o queries parametrizadas siempre
[ ] Validar y sanitizar todos los inputs con Pydantic/Zod
[ ] Escapar outputs que se renderizan en HTML
[ ] No ejecutar comandos de sistema con input del usuario
```

---

### A05 — Security Misconfiguration

```python
# ❌ CORS wildcard en producción
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# ✅ CORS estricto
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://miapp.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
)

# ✅ Headers de seguridad obligatorios
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response
```

**Checklist A05:**
```
[ ] CORS configurado con lista blanca, no wildcard en producción
[ ] Headers de seguridad: HSTS, X-Frame-Options, CSP, X-Content-Type-Options
[ ] Errores genéricos al usuario (no exponer stack traces)
[ ] Endpoints de debug/admin deshabilitados en producción
[ ] Dependencias sin usar eliminadas
[ ] Versiones de frameworks y librerías actualizadas
```

---

### A07 — Authentication Failures

```python
# ✅ JWT con refresh tokens y rotación
ACCESS_TOKEN_EXPIRY = timedelta(minutes=15)
REFRESH_TOKEN_EXPIRY = timedelta(days=7)

# ✅ Rate limiting en endpoints de auth
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.post("/auth/login")
@limiter.limit("5/minute")  # max 5 intentos por minuto
async def login(request: Request, credentials: LoginDTO):
    ...

# ✅ Invalidar todos los tokens en logout
async def logout(token: str, redis: Redis):
    await redis.setex(f"blacklist:{token}", ACCESS_TOKEN_EXPIRY, "1")
```

**Checklist A07:**
```
[ ] Tokens con expiración corta (15 min access, 7 días refresh)
[ ] Rate limiting en /login, /register, /forgot-password
[ ] Refresh tokens rotados en cada uso
[ ] Tokens invalidados en logout
[ ] Contraseñas con mínimo de complejidad validado
[ ] MFA disponible para cuentas de alto privilegio
[ ] No exponer si el email existe o no en mensajes de error
```

---

### A09 — Logging & Monitoring Failures

```python
# ✅ Logs estructurados (JSON para producción)
import structlog
logger = structlog.get_logger()

# ✅ Log de eventos de seguridad
logger.info("auth.login_success", user_id=user.id, ip=request.client.host)
logger.warning("auth.login_failed", email=email, ip=request.client.host)
logger.error("auth.unauthorized_access",
             user_id=current_user.id,
             resource=f"/users/{target_id}")

# ❌ NUNCA loggear datos sensibles
logger.info("user_data", password=password)  # ← NUNCA
logger.info("token", jwt=access_token)        # ← NUNCA
```

**Checklist A09:**
```
[ ] Logs estructurados en JSON para producción
[ ] Log de: autenticaciones exitosas/fallidas, accesos denegados, cambios de datos críticos
[ ] NO loggear: contraseñas, tokens, PII completa (solo últimos 4 dígitos)
[ ] Logs con timestamp, user_id, IP, acción
[ ] Alertas configuradas para: múltiples fallos de login, accesos desde IPs nuevas
```

---

## Vulnerabilidades en Dependencias

```bash
# Python
pip-audit
safety check

# Node.js
npm audit
npm audit fix

# Snyk (multi-plataforma)
snyk test
snyk monitor
```

**Política de dependencias:**
```
[ ] Auditar dependencias en cada PR (GitHub Actions)
[ ] Dependencias con CVE crítico → parchar en máximo 24 horas
[ ] Dependencias con CVE alto → parchar en máximo 1 semana
[ ] Revisar licencias de dependencias nuevas
[ ] Fijar versiones exactas en producción (no usar ^)
```

---

## Formato de Reporte de Auditoría de Seguridad

```markdown
## Auditoría de Seguridad — [Proyecto] — [Fecha]

### Resumen
- Vulnerabilidades críticas: X
- Vulnerabilidades altas: X
- Vulnerabilidades medias: X

### Hallazgos

| # | Vulnerabilidad | OWASP | Severidad | Archivo | Línea | Fix recomendado |
|---|---------------|-------|-----------|---------|-------|-----------------|
| 1 | SQL Injection | A03 | 🔴 Crítico | user.py | 45 | Usar query parametrizada |

### Dependencias vulnerables
| Paquete | Versión actual | CVE | Severidad | Acción |
|---------|---------------|-----|-----------|--------|

### Recomendaciones prioritarias
1. [Acción con responsable y fecha]
```

*Fuente: Antigravity Security Auditor Skill + OWASP Top 10 2021*
