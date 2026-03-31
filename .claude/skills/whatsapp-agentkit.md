# WhatsApp AgentKit — Skill para Cinthya y Sasha

## Descripcion
Skill para construir agentes de IA en WhatsApp en menos de 30 minutos usando Claude Code. Claude hace una entrevista de 10 preguntas sobre el negocio y genera el proyecto completo automaticamente. Stack: Python 3.11+, Anthropic API, WhatsApp API (Whapi / Meta / Twilio).

## Instrucciones

Cuando el usuario pida construir un agente de WhatsApp, sigue estas directrices:

### Requisitos previos

| Requisito | Como obtenerlo |
|-----------|---------------|
| Python 3.11+ | python.org o `brew install python` |
| Claude Code | `npm install -g @anthropic-ai/claude-code` |
| Anthropic API Key | platform.anthropic.com |
| WhatsApp API | Ver proveedores abajo |

### Proveedores de WhatsApp API

| Proveedor | Mejor para | Precio | Facilidad |
|-----------|-----------|--------|-----------|
| **Whapi.cloud** | Numero personal / pruebas rapidas | $10-30/mes | Alta |
| **Meta Cloud API** | Produccion con numero oficial | Gratis (hasta 1000 conv/mes) | Media |
| **Twilio** | Empresas con volumen alto | Variable por mensaje | Alta |

Recomendacion inicial: **Whapi.cloud** para pruebas y MVP. **Meta Cloud API** para produccion.

### Setup del proyecto

```bash
# 1. Clonar repositorio
git clone [repo-url]
cd [directorio]

# 2. Preparar entorno
bash start.sh

# 3. Lanzar Claude Code
claude

# 4. Iniciar wizard
/build-agent
```

### Las 10 preguntas del wizard

Claude Code hace estas preguntas en orden. Preparar respuestas antes de comenzar:

1. **Nombre del negocio** — Como se llama la empresa/proyecto
2. **Descripcion del servicio** — Que hace el negocio en 2-3 oraciones
3. **Persona del agente** — Nombre y personalidad del bot (ej: "Maria, asesora amable y profesional")
4. **Horario de atencion** — Cuando responde el bot vs cuando escalar a humano
5. **Servicios/productos principales** — Lista de lo que ofrece
6. **Preguntas frecuentes** — Top 5-10 FAQs del negocio
7. **Archivos de conocimiento** — Documentos PDF, menus, catalogos (opcional)
8. **Flujo de escalacion** — A quien notificar si el bot no puede responder
9. **Credenciales WhatsApp API** — Token del proveedor elegido
10. **Anthropic API Key** — Clave de la API de Claude

### Arquitectura generada automaticamente

```
[Cliente WhatsApp]
        ↓
[Webhook URL]
        ↓
[Python Flask/FastAPI server]
        ↓
[Claude API (Anthropic)]
        ↓
[Knowledge base + contexto del negocio]
        ↓
[Respuesta → Cliente]
```

### Testing local

```bash
# El wizard genera el comando exacto, tipicamente:
python main.py

# Usar ngrok para exponer webhook localmente
ngrok http 5000
```

### Deploy a produccion

**Opcion A — Docker (servidor propio)**
```bash
docker build -t whatsapp-agent .
docker run -d -p 5000:5000 whatsapp-agent
```

**Opcion B — Railway (recomendado para empezar)**
1. Subir codigo a GitHub
2. Conectar repo en railway.app
3. Railway detecta Python y despliega automaticamente
4. Copiar URL publica como webhook en el proveedor WhatsApp

### Personalizacion post-lanzamiento (lenguaje natural)

```
# Ejemplos de comandos post-deploy en Claude Code:
"Cambia el tono del agente a mas formal"
"Agrega el servicio de instalaciones industriales al catalogo"
"Cuando pregunten por precios, siempre pedir el nombre primero"
"Migra el agente de Whapi a Meta Cloud API"
```

### Checklist de seguridad (Sasha)

- [ ] API keys en variables de entorno, nunca en codigo
- [ ] Webhook con verificacion de firma del proveedor
- [ ] Rate limiting para prevenir spam
- [ ] Logs de conversaciones con PII anonimizado
- [ ] Timeout en llamadas a Claude API (max 30s)
- [ ] Validacion de numero de telefono entrante
- [ ] Plan de fallback si Claude API no responde

### Casos de uso en la Agencia

- Agente de atencion al cliente 24/7 para clientes de Juan Camilo
- Bot de calificacion de leads (pregunta, clasifica, agenda reunion)
- Asistente de pedidos para negocios con catalogo
- Agente interno del equipo para notificaciones y alertas
- Bot de soporte tecnico nivel 1 (FAQ automaticas)
