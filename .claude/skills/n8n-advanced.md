# n8n Advanced — Complex Workflows para Data Pipelines & AI Agents

## Descripcion
Skill avanzada de n8n que extiende `n8n-expert.md` con patrones para data pipelines, AI agents, multi-step workflows, y orquestacion compleja. Cubre RAG pipelines, scheduled reporting, multi-channel notifications, y error recovery avanzado. Optimizada para Cinthya con soporte de Sasha.

## Instrucciones

Esta skill EXTIENDE `n8n-expert.md`. Consultar la skill base primero para fundamentos. Esta skill cubre patrones avanzados.

### AI Agent Node

n8n incluye un nodo AI Agent nativo que soporta tool calling y memoria:

```
Configuracion del AI Agent Node:

1. Agent Type: "Tools Agent" (recomendado para la mayoria de casos)
2. LLM: Seleccionar proveedor
   - Anthropic (Claude): Preferido para analisis complejos
   - OpenAI: Alternativa si Claude no disponible
   - Ollama: Para procesamiento local sin costo de API
3. Tools: Conectar herramientas que el agente puede usar
   - Calculator
   - Code (JavaScript/Python)
   - HTTP Request
   - Supabase query
   - Custom tools
4. Memory: Opcional, para conversaciones con contexto
   - Window Buffer Memory (ultimos N mensajes)
   - Supabase (persistente)
```

**Patron: AI Agent que analiza datos y decide acciones:**
```
[Webhook: datos nuevos]
  → [Supabase: Get historical data]
  → [AI Agent Node]
      LLM: Claude Sonnet
      Tools: [Calculator, Code, HTTP Request]
      System prompt: "Eres un analista de datos. Analiza los datos recibidos,
                      compara con historicos, identifica anomalias."
  → [Switch: segun decision del agent]
      → "alert": [Slack: Enviar alerta]
      → "report": [Code: Generate report] → [Gmail: Send]
      → "normal": [Supabase: Log result]
```

### RAG Pipeline en n8n

Para consultas sobre documentos o datos con contexto:

```
Fase 1 — Ingestion (una vez):
[Manual Trigger]
  → [Read CSV/PDF files]
  → [Split In Batches: 50]
  → [Code: Chunk text (500 tokens, 50 overlap)]
  → [HTTP Request: Embedding API (Anthropic/OpenAI)]
  → [Supabase: Insert into vector table (pgvector)]

Fase 2 — Query (cada consulta):
[Webhook: user question]
  → [HTTP Request: Embed question]
  → [Supabase: Vector similarity search (top 5)]
  → [Code: Build prompt with context]
  → [HTTP Request: Claude API]
  → [Webhook Response: answer]
```

**SQL para tabla de vectores en Supabase:**
```sql
-- Habilitar pgvector
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    metadata JSONB,
    embedding VECTOR(1536),  -- Dimension segun modelo de embedding
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indice para busqueda rapida
CREATE INDEX ON document_chunks USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Funcion de busqueda
CREATE OR REPLACE FUNCTION search_documents(
    query_embedding VECTOR(1536),
    match_threshold FLOAT DEFAULT 0.7,
    match_count INT DEFAULT 5
)
RETURNS TABLE (id UUID, content TEXT, metadata JSONB, similarity FLOAT)
LANGUAGE sql STABLE AS $$
    SELECT id, content, metadata,
           1 - (embedding <=> query_embedding) AS similarity
    FROM document_chunks
    WHERE 1 - (embedding <=> query_embedding) > match_threshold
    ORDER BY embedding <=> query_embedding
    LIMIT match_count;
$$;
```

### Data Pipeline Patterns

**Pattern 1: ETL (Extract, Transform, Load)**
```
[Schedule: daily 2am]
  → [HTTP Request: Extract from source API]
  → [Code: Transform data]
      // Limpiar, normalizar, enriquecer
      const items = $input.all();
      return items.map(item => ({
        json: {
          id: item.json.id,
          name: item.json.name?.trim().toLowerCase(),
          revenue: parseFloat(item.json.revenue) || 0,
          date: new Date(item.json.date).toISOString(),
          source: 'api_extraction',
          processed_at: new Date().toISOString()
        }
      }));
  → [Supabase: Upsert (load)]
  → [Code: Generate summary stats]
  → [Slack: Notify completion with stats]
```

**Pattern 2: CDC (Change Data Capture)**
```
[Supabase Trigger: row changed in 'orders']
  → [Switch: insert/update/delete]
      → insert: [Code: Enrich new order] → [Supabase: Update analytics] → [Slack: New order alert]
      → update: [IF: status changed?]
          → YES: [Code: Calculate SLA] → [Supabase: Update SLA metrics]
          → NO: [No Op]
      → delete: [Supabase: Archive to deleted_orders]
```

**Pattern 3: Fan-out / Fan-in**
```
[Trigger]
  → [Split In Batches: 5]
  → [Parallel execution via sub-workflows]
      → [Execute Workflow: process-batch-1]
      → [Execute Workflow: process-batch-2]
      → [Execute Workflow: process-batch-3]
  → [Merge: Wait for all]
  → [Code: Aggregate results]
  → [Output]
```

### Multi-Channel Notification System

```
[Trigger: event]
  → [Supabase: Get user notification preferences]
  → [Switch: channel preference]
      → "email": [Gmail: Send email]
      → "slack": [Slack: Send DM]
      → "whatsapp": [HTTP Request: Whapi API]
      → "telegram": [Telegram: Send message]
      → "push": [HTTP Request: OneSignal/Firebase]
      → "all": [Execute Workflow: send-to-all-channels]
  → [Supabase: Log notification sent]
```

### Scheduled Reporting System

Para Data Reporting Agents, el sistema de reportes programados:

```
Workflow: Scheduled Report Generator

[Schedule: every 15 min]
  → [Supabase: Get reports WHERE next_run <= NOW() AND is_active = true]
  → [IF: reports found?]
      → NO: [Stop]
      → YES:
        → [Split In Batches: 1 report at a time]
        → [HTTP Request: GET FastAPI /api/v1/analysis/latest?dashboard_id=X]
        → [Code: Build HTML email]
            const analysis = $input.first().json;
            const report = $('Supabase').first().json;
            
            const html = `
            <div style="font-family: Inter, sans-serif; max-width: 600px; margin: 0 auto;">
              <h1 style="color: #1E293B;">${report.name}</h1>
              <p style="color: #64748B;">Generated ${new Date().toLocaleDateString()}</p>
              
              <div style="background: #F8FAFC; border-radius: 12px; padding: 24px; margin: 16px 0;">
                <h2>Summary</h2>
                <p>${analysis.summary}</p>
              </div>
              
              <div style="margin: 16px 0;">
                <h2>Key Insights</h2>
                ${analysis.insights.map(i => `
                  <div style="border-left: 3px solid ${i.importance === 'high' ? '#EF4444' : '#2563EB'}; padding-left: 12px; margin: 8px 0;">
                    <strong>${i.title}</strong>
                    <p>${i.description}</p>
                  </div>
                `).join('')}
              </div>
              
              <div style="margin: 16px 0;">
                <h2>Recommendations</h2>
                ${analysis.recommendations.map(r => `
                  <p>→ ${r.action} (${r.priority} priority)</p>
                `).join('')}
              </div>
              
              <p style="color: #94A3B8; font-size: 12px;">
                Powered by Data Reporting Agents | <a href="https://app.example.com">View Dashboard</a>
              </p>
            </div>`;
            
            return [{ json: { html, subject: `${report.name} — ${new Date().toLocaleDateString()}` }}];
        → [Split In Batches: recipients]
        → [Gmail: Send to each recipient]
        → [Supabase: Update last_sent_at and calculate next_run]
```

### Error Recovery Avanzado

**Pattern: Circuit Breaker**
```
[Trigger]
  → [Supabase: Check circuit breaker status for service X]
  → [IF: circuit open?]
      → YES: [Webhook Response: 503 Service Unavailable] → [Stop]
      → NO:
        → [HTTP Request: Call service X]
            On success:
              → [Supabase: Reset failure count]
              → [Continue normal flow]
            On error:
              → [Supabase: Increment failure count]
              → [IF: failure_count >= 5]
                  → YES: [Supabase: Open circuit (set open_until = NOW() + 5min)]
                         [Slack: Alert — circuit opened for service X]
                  → NO: [Wait: 1s] → [Retry]
```

**Pattern: Dead Letter Queue**
```
[Main Workflow]
  → [Process items...]
  → On error:
    → [Supabase: Insert into dead_letter_queue]
        {original_payload, error_message, workflow_id, retry_count: 0, created_at}
    → [Continue with next item]

[Schedule: every 30min] — DLQ Processor
  → [Supabase: Get items WHERE retry_count < 3 AND created_at > NOW() - 24h]
  → [Split In Batches]
  → [Execute Workflow: original workflow]
  → On success: [Supabase: Delete from DLQ]
  → On error: [Supabase: Increment retry_count]
              [IF: retry_count >= 3]
                → [Slack: Alert — permanent failure, manual intervention needed]
```

### Webhook Security Avanzada

```javascript
// Nodo Code: Validar webhook signature (HMAC)
const crypto = require('crypto');

const payload = JSON.stringify($input.first().json);
const signature = $input.first().headers['x-webhook-signature'];
const secret = $env.WEBHOOK_SECRET;

const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex');

if (signature !== `sha256=${expectedSignature}`) {
    throw new Error('Invalid webhook signature');
}

return $input.all();
```

### Performance Optimization

1. **Batch processing**: Siempre usar Split In Batches para listas grandes (max 50 items por batch).
2. **Sub-workflows**: Workflows con mas de 15 nodos deben dividirse.
3. **Caching**: Usar nodo Code con variables estaticas para cache en memoria dentro de una ejecucion.
4. **Timeout tuning**: HTTP Requests a APIs lentas: timeout 120s. A APIs rapidas: 10s.
5. **Execution mode**: Para workflows de alto volumen, usar mode "queue" en n8n config.

### n8n Config para Produccion

```env
# .env para n8n en Railway/Docker
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=secure_password_here
EXECUTIONS_MODE=queue
EXECUTIONS_DATA_SAVE_ON_ERROR=all
EXECUTIONS_DATA_SAVE_ON_SUCCESS=none
EXECUTIONS_DATA_SAVE_MANUAL_EXECUTIONS=true
EXECUTIONS_DATA_PRUNE=true
EXECUTIONS_DATA_MAX_AGE=168  # 7 days
N8N_ENCRYPTION_KEY=random_32_char_string
WEBHOOK_URL=https://n8n.yourdomain.com/
N8N_DIAGNOSTICS_ENABLED=false
N8N_VERSION_NOTIFICATIONS_ENABLED=false
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=db.supabase.co
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n
DB_POSTGRESDB_USER=n8n_user
DB_POSTGRESDB_PASSWORD=secure_password
```

### Integracion con Data Reporting Agents

Cinthya implementa estos 4 workflows para el MVP:

| Workflow | Trigger | Funcion | Priority |
|----------|---------|---------|----------|
| `email-report.json` | Schedule (cron from DB) | Enviar reportes por email | P0 |
| `alert-threshold.json` | Schedule (hourly) | Alertar cuando metrica cruza umbral | P1 |
| `data-ingestion.json` | Webhook | Recibir datos de fuentes externas | P1 |
| `weekly-summary.json` | Schedule (Mon 9am) | Resumen semanal al admin | P2 |

### Mejores Practicas Avanzadas

1. **Idempotencia**: Todo webhook debe ser idempotente. Usar `idempotency_key` en payloads.
2. **Observabilidad**: Agregar nodo de logging al inicio y fin de cada workflow critico.
3. **Version control**: Exportar workflows como JSON al repo Git despues de cada cambio.
4. **Testing**: Crear workflow `test-*` mirror para cada workflow de produccion con datos fake.
5. **Secrets rotation**: Nunca hardcodear. Usar credenciales de n8n + env vars. Rotar cada 90 dias.
6. **Graceful degradation**: Si un servicio externo falla, el workflow debe continuar con los demas.
7. **Rate limiting propio**: Usar nodo Wait entre llamadas a APIs con rate limits estrictos.
8. **Monitoring**: Workflow dedicado que monitorea ejecuciones fallidas y alerta via Slack.
