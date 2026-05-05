# ASTECIA — WhatsApp Web Integration

**ASTECIA en WhatsApp Web**: Tu asesor comercial estratégico siempre disponible. Responde órdenes en tiempo real usando Claude API.

---

## ¿Qué es esto?

ASTECIA escucha tus mensajes en WhatsApp Web y responde automáticamente con:
- ✅ Análisis de oportunidades comerciales
- ✅ Investigación de clientes (perfiles, dolores, tomadores de decisión)
- ✅ Redacción de emails y guiones persuasivos
- ✅ Estrategia de ventas (AIDA, SPIN Selling, PNL)
- ✅ Manejo de objeciones
- ✅ Priorización de pipeline

**Ejemplo de uso:**
```
Tú:      "@astecia ¿Vale la pena perseguir a Prokpil?"
ASTECIA: "No. Lleva 4 meses, decision maker cambió, presupuesto congelado. 
          Cancela hoy, enfócate en Papeles del Cauca (cierre mes). ¿Acción confirmada?"
```

---

## Requisitos

1. **Node.js 18+** — [Descargar](https://nodejs.org/)
2. **Antropic API Key** — [Obtener en anthropic.com](https://console.anthropic.com)
3. **WhatsApp Web abierto** en tu navegador (Chrome, Edge, Firefox)

---

## Instalación

### 1. Clonar y setup del proyecto

```bash
cd whatsapp-astecia
npm install
```

### 2. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env
```

Editar `.env` y agregar tu API Key de Anthropic:
```env
ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Ejecutar ASTECIA

```bash
npm start
```

**Primera ejecución:**
- Aparecerá un **código QR en la terminal**
- Abre WhatsApp Web en tu navegador: [web.whatsapp.com](https://web.whatsapp.com)
- Escanea el QR con tu teléfono (Menú → Dispositivos vinculados → Vincular dispositivo)
- ASTECIA se activará automáticamente

---

## Uso

Una vez conectado, **menciona ASTECIA al inicio de tu mensaje** y ella responderá:

```
📱 Llamadas válidas (ASTECIA responde):

✅ "Astecia ¿Vale la pena Cargill?"
✅ "@astecia Redacta email para Omnilife"
✅ "ASTECIA ¿Quién es el decision maker en Colombina?"
✅ "astecia Argumentario vs: 'Es muy caro'"
✅ "Astecia ¿Cuántos deals puedo cerrar en 60 días?"
✅ "@astecia Estructura propuesta para 80M COP"

❌ Mensajes ignorados (ASTECIA NO responde):

❌ "¿Vale la pena Cargill?" (sin mencionar ASTECIA)
❌ "Redacta email para Omnilife" (sin mencionar ASTECIA)
```

**ASTECIA responderá automáticamente en el chat.**

### Formatos válidos para llamar a ASTECIA:
- `astecia ...` (minúsculas)
- `Astecia ...` (mayúscula inicial)
- `ASTECIA ...` (mayúsculas)
- `@astecia ...` (con arroba)

---

## Características

### ✅ Metodologías Integradas
- **PNL**: Lenguaje persuasivo, metáforas, reencuadre
- **AIDA**: Atención → Interés → Deseo → Acción
- **SPIN Selling**: Diagnóstico consultivo (Situación → Problema → Implicación → Necesidad)
- **Modelo DISC**: Adaptación por perfil (Dominante, Influyente, Estable, Concienzudo)
- **Witty**: Ingenioso, que engancha desde la primera frase

### 🧠 Las 3 Facetas de ASTECIA
- **LEO (Vendedor)**: Cierra deals, redacta persuasivo, maneja objeciones
- **YANG (Investigadora)**: Analiza clientes, identifica dolores, mapea decisión
- **JARVIS (Estratega)**: Evalúa portfolio, prioriza, ve el cuadro completo

### ⚡ Respuestas Rápidas
- Máximo 3 párrafos (formato WhatsApp)
- Siempre accionables (siguiente paso concreto)
- Sinceras (te dirá si algo no va a cerrar)
- En español únicamente

---

## Archivos del Proyecto

```
whatsapp-astecia/
├── astecia-whatsapp.js       ← Script principal
├── package.json              ← Dependencias Node.js
├── .env.example              ← Plantilla de configuración
├── .env                       ← Tu configuración (SECRETO)
├── README.md                 ← Este archivo
├── utils/
│   └── astecia-prompt.js     ← Prompt system de ASTECIA
└── sessions/
    └── astecia-session/      ← Auto-creado: datos de sesión
        ├── pre-key-*.json
        ├── app-state-sync-*.json
        └── ...
```

---

## Solución de Problemas

### ❌ "ANTHROPIC_API_KEY no configurada"
```bash
# Editar .env y agregar tu API key
ANTHROPIC_API_KEY=sk-ant-YOUR_KEY_HERE
```

### ❌ "QR no aparece"
- Asegúrate de ejecutar desde terminal/CMD
- Si ya estaba conectado, borra la carpeta `sessions/` y intenta de nuevo:
  ```bash
  rm -rf sessions/
  npm start
  ```

### ❌ "ASTECIA no responde"
- Verifica que WhatsApp Web esté abierto en tu navegador
- Revisa que la sesión esté activa (deberías ver "ASTECIA está activo en WhatsApp Web")
- Algunos mensajes pueden tomar 5-10 segundos (depende de internet)

### ❌ "Module not found: '@whiskeysockets/baileys'"
```bash
# Reinstalar dependencias
rm -rf node_modules package-lock.json
npm install
```

---

## Ejemplos de Conversación Real

```
Tú:      "Astecia ¿Vale la pena perseguir a Prokpil?"
ASTECIA: "No. Lleva 4 meses, decision maker cambió, presupuesto congelado. 
          Cancela hoy, enfócate en Papeles del Cauca (cierre mes). ¿Acción confirmada?"

Tú:      "astecia Redacta email para Omnilife post-demo"
ASTECIA: "Asunto: Demo exitosa — Siguientes pasos ⚡

Hola Omnilife,
Gracias por la demo de hoy. Los resultados hablan solos:
- Reducción de 40% en tiempo de codificación
- Cero rechazos de producto
- ROI en 6 meses

La propuesta técnica está lista. ¿Podemos cerrar esto esta semana?

Confirmación urgente,
Juan Camilo"

Tú:      "@astecia ¿Quién es el decision maker en Colombina?"
ASTECIA: "Perfil DISC = C (Concienzudo). 
          Decision maker: Gerente de Operaciones + CFO (binomio).
          Estrategia: datos, ROI probado, sin presión. 
          Momento: después de resolver problema tinta (en 2 semanas)."
```

## Desarrollo Local

### Modo watch (auto-reinicia al cambiar archivos)
```bash
npm run dev
```

### Aumentar verbosidad de logs
Editar `.env`:
```env
LOG_LEVEL=debug
```

---

## Seguridad

⚠️ **IMPORTANTE:**

1. **`.env` es secreto** — Nunca lo commits a GitHub
2. **`sessions/` contiene datos sensibles** — Nunca lo compartas
3. **API Key de Anthropic es privada** — Guárdala bien
4. `.gitignore` ya los excluye (verificar antes de push)

---

## Configuración Avanzada

### Cambiar modelo Claude
```env
ASTECIA_MODEL=claude-sonnet-4-20250514  # Más potente pero más lento
```

### Cambiar máximo de tokens
```env
ASTECIA_MAX_TOKENS=2048  # Por defecto: 1024
```

### Usar sesión diferente
```env
WHATSAPP_SESSION_NAME=astecia-alt
```

---

## Roadmap

- [ ] Soporte para grupos (responder a menciones @astecia)
- [ ] Historial de conversaciones persistente
- [ ] Análisis de attachments (fotos de documentos)
- [ ] Integración con portfolio MAPER (CRM sync)
- [ ] Webhooks para automatización externa
- [ ] Dashboard de métricas (mensajes procesados, respuestas)

---

## Soporte

Si hay errores:
1. Revisa la salida de la terminal (hay logs detallados)
2. Verifica que Node.js 18+ esté instalado: `node --version`
3. Confirma que Anthropic API Key está correcta
4. Intenta eliminar `sessions/` y volver a conectar

---

## Sobre ASTECIA

ASTECIA es tu asesor comercial estratégico, especializado en:
- 🎯 Ventas B2B industriales (CIJ, TIJ, Laser, Automatización)
- 💬 Redacción persuasiva y argumentarios de cierre
- 📊 Análisis de oportunidades y pipeline
- 🎭 Adaptación de mensajes por perfil DISC
- ⚡ Respuestas instantáneas, accionables, sinceras

**"Sin demora, sin teoría, sin relleno."**

---

## Licencia

Uso privado — Juan Camilo Gil. MAPER S.A.

---

**Última actualización:** 2026-04-17  
**Creado por:** Jarvis (CEO, Agencia de Agentes IA)
