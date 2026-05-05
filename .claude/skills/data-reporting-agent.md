# Data Reporting Agent — MVP Architecture & Implementation

## Descripcion
Skill para construir el producto SaaS "Data Reporting Agents": upload de datos, analisis automatizado con Claude, dashboard interactivo y reportes por email. Stack: FastAPI backend + Next.js frontend + n8n workflows + Supabase. Target: $300-480k ARR.

## Instrucciones

Cuando el usuario trabaje en el proyecto Data Reporting Agents, sigue estas directrices:

### Vision del Producto

**Pitch**: "Sube tus datos. La IA los analiza. Recibe insights y dashboards interactivos."

**Flujo del usuario:**
```
1. Upload CSV/Excel/conectar DB
2. IA analiza automaticamente (Claude Opus)
3. Dashboard interactivo con charts
4. Preguntas en lenguaje natural sobre los datos
5. Reportes por email (programados o ad-hoc)
6. Alertas cuando metricas cambian significativamente
```

### Arquitectura del Sistema

```
                    +------------------+
                    |  Next.js Frontend |
                    |  (Vercel)         |
                    +--------+---------+
                             |
                    +--------v---------+
                    |  FastAPI Backend  |
                    |  (Railway)        |
                    +--------+---------+
                             |
            +----------------+----------------+
            |                |                |
   +--------v------+  +-----v-------+  +-----v-------+
   | Supabase      |  | Claude API  |  | n8n         |
   | (PostgreSQL + |  | (Analysis)  |  | (Workflows) |
   | Storage +     |  |             |  |             |
   | Auth + RLS)   |  +-------------+  +-------------+
   +---------------+
```

### Estructura del Proyecto

```
data-reporting-agents/
  backend/
    app/
      main.py
      config.py
      dependencies.py
      core/
        security.py
        exceptions.py
        middleware.py
      api/
        v1/
          router.py
          endpoints/
            auth.py
            datasets.py        # Upload, list, delete datasets
            analysis.py        # Trigger analysis, get insights
            dashboards.py      # CRUD dashboards
            reports.py         # Scheduled reports
            chat.py            # Natural language Q&A sobre datos
      models/
        dataset.py
        analysis.py
        dashboard.py
        report.py
      schemas/
        dataset.py
        analysis.py
        dashboard.py
        report.py
        chat.py
      services/
        dataset_service.py     # Parse CSV/Excel, validate, store
        analysis_service.py    # Claude API integration
        dashboard_service.py   # Chart generation
        report_service.py      # Email scheduling
        chat_service.py        # Natural language queries
      repositories/
        dataset_repository.py
        analysis_repository.py
      utils/
        data_parser.py         # CSV/Excel parsing
        chart_generator.py     # Chart config generation
        email_sender.py        # Transactional emails
    tests/
    requirements.txt
    Dockerfile
    
  frontend/
    src/
      app/
        page.tsx               # Landing / login
        dashboard/
          page.tsx             # Main dashboard
          [id]/page.tsx        # Specific dashboard view
        datasets/
          page.tsx             # Dataset list
          upload/page.tsx      # Upload flow
        analysis/
          [id]/page.tsx        # Analysis results
        reports/
          page.tsx             # Report management
        chat/
          page.tsx             # Natural language Q&A
      components/
        ui/                    # shadcn/ui components
        charts/                # Chart components (Recharts)
        layout/                # Header, sidebar, footer
        datasets/              # Upload, preview, table
        analysis/              # Insight cards, summaries
      lib/
        api.ts                 # API client (fetch wrapper)
        auth.ts                # Supabase auth
        utils.ts
      types/
        index.ts
    package.json
    tailwind.config.ts
    next.config.ts
    
  n8n/
    workflows/
      email-report.json        # Scheduled email reports
      alert-threshold.json     # Alert when metric crosses threshold
      data-ingestion.json      # Webhook for external data sources
      weekly-summary.json      # Weekly summary email
```

### Base de Datos (Supabase)

```sql
-- Datasets
CREATE TABLE datasets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),
    name TEXT NOT NULL,
    description TEXT,
    file_url TEXT NOT NULL,           -- Supabase Storage URL
    file_type TEXT NOT NULL,          -- csv, xlsx, json
    row_count INTEGER,
    column_count INTEGER,
    columns JSONB,                    -- [{name, type, sample_values}]
    size_bytes BIGINT,
    status TEXT DEFAULT 'uploaded',   -- uploaded, processing, ready, error
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Analyses
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset_id UUID NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id),
    summary TEXT,                      -- AI-generated summary
    insights JSONB,                    -- [{title, description, type, importance}]
    statistics JSONB,                  -- {mean, median, std, correlations, etc.}
    recommendations JSONB,             -- [{action, rationale, priority}]
    model_used TEXT DEFAULT 'claude-opus-4-20250514',
    tokens_used INTEGER,
    status TEXT DEFAULT 'pending',     -- pending, processing, completed, error
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Dashboards
CREATE TABLE dashboards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),
    name TEXT NOT NULL,
    description TEXT,
    dataset_id UUID REFERENCES datasets(id),
    charts JSONB,                      -- [{type, config, position, size}]
    layout JSONB,                      -- Grid layout configuration
    is_public BOOLEAN DEFAULT FALSE,
    share_token TEXT UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Reports
CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),
    dashboard_id UUID REFERENCES dashboards(id),
    name TEXT NOT NULL,
    schedule TEXT,                     -- Cron expression: "0 9 * * 1" (Mon 9am)
    recipients JSONB,                 -- [{email, name}]
    format TEXT DEFAULT 'html',       -- html, pdf
    last_sent_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Chat messages (natural language Q&A)
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id),
    dataset_id UUID NOT NULL REFERENCES datasets(id),
    role TEXT NOT NULL,                -- user, assistant
    content TEXT NOT NULL,
    metadata JSONB,                   -- {sql_generated, chart_generated, tokens_used}
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policies
ALTER TABLE datasets ENABLE ROW LEVEL SECURITY;
ALTER TABLE analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE dashboards ENABLE ROW LEVEL SECURITY;
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users see own datasets" ON datasets
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users see own analyses" ON analyses
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users see own dashboards" ON dashboards
    FOR ALL USING (auth.uid() = user_id OR is_public = true);

CREATE POLICY "Users see own reports" ON reports
    FOR ALL USING (auth.uid() = user_id);

CREATE POLICY "Users see own chat" ON chat_messages
    FOR ALL USING (auth.uid() = user_id);
```

### Servicio de Analisis con Claude

```python
# app/services/analysis_service.py
import anthropic
import json
from uuid import UUID

from app.config import get_settings
from app.repositories.dataset_repository import DatasetRepository
from app.repositories.analysis_repository import AnalysisRepository

settings = get_settings()

class AnalysisService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.dataset_repo = DatasetRepository()
        self.analysis_repo = AnalysisRepository()
    
    async def analyze_dataset(self, dataset_id: UUID, user_id: UUID) -> dict:
        """Analiza un dataset completo con Claude Opus."""
        
        # 1. Obtener metadata y sample del dataset
        dataset = await self.dataset_repo.get_by_id(dataset_id)
        if not dataset or dataset["user_id"] != str(user_id):
            raise PermissionError("Dataset not found or access denied")
        
        sample_data = await self.dataset_repo.get_sample_rows(dataset_id, limit=100)
        columns = dataset["columns"]
        
        # 2. Construir prompt para analisis
        prompt = f"""You are a senior data analyst. Analyze this dataset thoroughly.

DATASET: {dataset['name']}
ROWS: {dataset['row_count']}
COLUMNS: {json.dumps(columns, indent=2)}

SAMPLE DATA (first 100 rows):
{json.dumps(sample_data, indent=2)}

Provide your analysis in this exact JSON format:
{{
    "summary": "2-3 paragraph executive summary of the dataset",
    "insights": [
        {{
            "title": "Insight title",
            "description": "Detailed description",
            "type": "trend|anomaly|correlation|distribution|comparison",
            "importance": "high|medium|low",
            "affected_columns": ["col1", "col2"]
        }}
    ],
    "statistics": {{
        "numeric_columns": {{
            "column_name": {{
                "mean": 0, "median": 0, "std": 0, "min": 0, "max": 0,
                "quartiles": [0, 0, 0]
            }}
        }},
        "categorical_columns": {{
            "column_name": {{
                "unique_values": 0,
                "top_values": [{{"value": "x", "count": 0}}],
                "null_percentage": 0
            }}
        }},
        "correlations": [{{"col1": "x", "col2": "y", "correlation": 0.0, "strength": "strong|moderate|weak"}}]
    }},
    "recommendations": [
        {{
            "action": "What to do",
            "rationale": "Why",
            "priority": "high|medium|low"
        }}
    ],
    "suggested_charts": [
        {{
            "type": "bar|line|scatter|pie|area|heatmap",
            "title": "Chart title",
            "x_axis": "column_name",
            "y_axis": "column_name",
            "description": "What this chart shows"
        }}
    ]
}}

Be specific with numbers. Reference actual column names and values from the data."""

        # 3. Llamar a Claude Opus
        response = self.client.messages.create(
            model="claude-opus-4-20250514",
            max_tokens=8192,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # 4. Parsear respuesta
        response_text = response.content[0].text
        # Extraer JSON del response (puede venir envuelto en markdown)
        json_start = response_text.find("{")
        json_end = response_text.rfind("}") + 1
        analysis_data = json.loads(response_text[json_start:json_end])
        
        # 5. Guardar en DB
        analysis = await self.analysis_repo.create({
            "dataset_id": str(dataset_id),
            "user_id": str(user_id),
            "summary": analysis_data["summary"],
            "insights": analysis_data["insights"],
            "statistics": analysis_data["statistics"],
            "recommendations": analysis_data["recommendations"],
            "model_used": "claude-opus-4-20250514",
            "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
            "status": "completed",
        })
        
        return {**analysis, "suggested_charts": analysis_data.get("suggested_charts", [])}
```

### Servicio de Chat (Natural Language Q&A)

```python
# app/services/chat_service.py
import anthropic
import json
from uuid import UUID

from app.config import get_settings
from app.repositories.dataset_repository import DatasetRepository
from app.repositories.chat_repository import ChatRepository

settings = get_settings()

class ChatService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.dataset_repo = DatasetRepository()
        self.chat_repo = ChatRepository()
    
    async def ask(self, dataset_id: UUID, user_id: UUID, question: str) -> dict:
        """Responde preguntas en lenguaje natural sobre un dataset."""
        
        dataset = await self.dataset_repo.get_by_id(dataset_id)
        columns = dataset["columns"]
        sample = await self.dataset_repo.get_sample_rows(dataset_id, limit=50)
        
        # Obtener historial de chat reciente
        history = await self.chat_repo.get_recent(dataset_id, user_id, limit=10)
        
        messages = []
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        system_prompt = f"""You are a data analyst assistant. The user has a dataset with these characteristics:

DATASET: {dataset['name']}
ROWS: {dataset['row_count']}
COLUMNS: {json.dumps(columns)}
SAMPLE: {json.dumps(sample[:10])}

Answer questions about this data. When relevant:
1. Provide specific numbers and percentages
2. Suggest visualizations (respond with chart_config JSON if a chart would help)
3. Explain trends and patterns
4. Be concise but thorough

If a chart would help illustrate the answer, include it as:
[CHART]{{"type": "bar", "title": "...", "x": "col", "y": "col", "data": [...]}}[/CHART]"""

        messages.append({"role": "user", "content": question})
        
        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",  # Sonnet para velocidad en chat
            max_tokens=2048,
            system=system_prompt,
            messages=messages,
        )
        
        answer = response.content[0].text
        
        # Guardar en historial
        await self.chat_repo.create(dataset_id, user_id, "user", question)
        await self.chat_repo.create(dataset_id, user_id, "assistant", answer, {
            "tokens_used": response.usage.input_tokens + response.usage.output_tokens
        })
        
        # Extraer chart config si existe
        chart_config = None
        if "[CHART]" in answer:
            chart_start = answer.index("[CHART]") + 7
            chart_end = answer.index("[/CHART]")
            chart_config = json.loads(answer[chart_start:chart_end])
            answer = answer[:answer.index("[CHART]")] + answer[chart_end + 8:]
        
        return {
            "answer": answer.strip(),
            "chart": chart_config,
        }
```

### Frontend — Dashboard con Charts

```typescript
// frontend/src/components/charts/DynamicChart.tsx
"use client";

import {
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  ScatterChart, Scatter, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from "recharts";

interface ChartConfig {
  type: "bar" | "line" | "pie" | "scatter" | "area";
  title: string;
  x_axis: string;
  y_axis: string;
  data: Record<string, unknown>[];
  colors?: string[];
}

const DEFAULT_COLORS = ["#2563EB", "#F59E0B", "#10B981", "#EF4444", "#8B5CF6", "#EC4899"];

export function DynamicChart({ config }: { config: ChartConfig }) {
  const colors = config.colors || DEFAULT_COLORS;

  const renderChart = () => {
    switch (config.type) {
      case "bar":
        return (
          <BarChart data={config.data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={config.x_axis} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey={config.y_axis} fill={colors[0]} />
          </BarChart>
        );
      case "line":
        return (
          <LineChart data={config.data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={config.x_axis} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey={config.y_axis} stroke={colors[0]} />
          </LineChart>
        );
      case "pie":
        return (
          <PieChart>
            <Pie data={config.data} dataKey={config.y_axis} nameKey={config.x_axis} cx="50%" cy="50%" outerRadius={120}>
              {config.data.map((_, index) => (
                <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        );
      case "scatter":
        return (
          <ScatterChart>
            <CartesianGrid />
            <XAxis dataKey={config.x_axis} name={config.x_axis} />
            <YAxis dataKey={config.y_axis} name={config.y_axis} />
            <Tooltip cursor={{ strokeDasharray: "3 3" }} />
            <Scatter data={config.data} fill={colors[0]} />
          </ScatterChart>
        );
      case "area":
        return (
          <AreaChart data={config.data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey={config.x_axis} />
            <YAxis />
            <Tooltip />
            <Area type="monotone" dataKey={config.y_axis} stroke={colors[0]} fill={colors[0]} fillOpacity={0.3} />
          </AreaChart>
        );
      default:
        return <p>Unsupported chart type: {config.type}</p>;
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{config.title}</h3>
      <ResponsiveContainer width="100%" height={400}>
        {renderChart()}
      </ResponsiveContainer>
    </div>
  );
}
```

### n8n Workflows

**1. Email Report (scheduled):**
```
[Schedule Trigger: cron from DB] 
  → [Supabase: Get active reports] 
  → [Split In Batches] 
  → [HTTP Request: FastAPI /analysis/latest?dashboard_id=X]
  → [Code: Build HTML email with charts]
  → [Gmail: Send to recipients]
  → [Supabase: Update last_sent_at]
```

**2. Alert on Threshold:**
```
[Schedule: every 1h]
  → [Supabase: Get datasets with alerts]
  → [HTTP Request: FastAPI /analysis/check-thresholds]
  → [IF: threshold crossed]
    → YES: [Slack: Alert] + [Gmail: Notify user]
    → NO: [No Op]
```

**3. Data Ingestion Webhook:**
```
[Webhook: POST /ingest]
  → [Code: Validate payload]
  → [Supabase Storage: Save file]
  → [Supabase: Create dataset record]
  → [HTTP Request: FastAPI /analysis/trigger]
  → [Webhook Response: 202 Accepted]
```

### API Endpoints (FastAPI)

```
POST   /api/v1/auth/register          # Registro
POST   /api/v1/auth/login             # Login → JWT
POST   /api/v1/auth/refresh           # Refresh token

GET    /api/v1/datasets               # Listar datasets del usuario
POST   /api/v1/datasets/upload        # Upload CSV/Excel
GET    /api/v1/datasets/{id}          # Detalle de dataset
DELETE /api/v1/datasets/{id}          # Eliminar dataset
GET    /api/v1/datasets/{id}/preview  # Preview primeras 100 filas

POST   /api/v1/analysis/trigger       # Iniciar analisis
GET    /api/v1/analysis/{id}          # Resultado del analisis
GET    /api/v1/analysis/latest        # Ultimo analisis de un dataset

GET    /api/v1/dashboards             # Listar dashboards
POST   /api/v1/dashboards             # Crear dashboard
GET    /api/v1/dashboards/{id}        # Ver dashboard
PATCH  /api/v1/dashboards/{id}        # Actualizar charts/layout
DELETE /api/v1/dashboards/{id}        # Eliminar

GET    /api/v1/dashboards/shared/{token}  # Dashboard publico

POST   /api/v1/reports                # Crear reporte programado
GET    /api/v1/reports                # Listar reportes
PATCH  /api/v1/reports/{id}           # Actualizar schedule
DELETE /api/v1/reports/{id}           # Eliminar

POST   /api/v1/chat/{dataset_id}     # Preguntar sobre datos
GET    /api/v1/chat/{dataset_id}/history  # Historial de chat

GET    /health                        # Health check
```

### Pricing Tiers

| Feature | Starter ($299/mo) | Pro ($599/mo) | Enterprise ($999/mo) |
|---------|-------------------|---------------|---------------------|
| Datasets | 10 | 50 | Unlimited |
| Analysis/month | 20 | 100 | Unlimited |
| Chat messages | 100 | 500 | Unlimited |
| Dashboards | 5 | 25 | Unlimited |
| Scheduled reports | 2 | 10 | Unlimited |
| Max file size | 50MB | 200MB | 1GB |
| API access | No | Yes | Yes + Webhooks |
| Support | Email | Priority | Dedicated |
| Data retention | 30 days | 90 days | Unlimited |

### Milestones

| Semana | Entregable | Owner |
|--------|-----------|-------|
| 2 | Architecture finalized, DB schema, API spec | Alejo + Sasha |
| 3 | Auth + Dataset upload + Storage | Sasha |
| 4 | Analysis service (Claude integration) | Sasha |
| 4 | Frontend: auth + upload + dataset list | Brook |
| 5 | Chat service + Dashboard service | Sasha |
| 5 | Frontend: analysis view + charts | Brook |
| 6 | n8n: email reports + alerts | Cinthya |
| 6 | Frontend: dashboard builder + reports | Brook |
| 7 | Integration testing + polish | All |
| 8 | Beta launch + 3 pilots onboarded | Leo + All |

### Tech Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Backend framework | FastAPI | Async, auto-docs, Pydantic, Python + Claude SDK |
| Frontend framework | Next.js 15 | SSR, App Router, React Server Components |
| CSS | Tailwind CSS 4 | Consistent with Agencia stack |
| Charts | Recharts | React-native, lightweight, customizable |
| Database | Supabase (PostgreSQL) | Auth, RLS, Storage, Realtime built-in |
| File storage | Supabase Storage | Integrated with DB, RLS-protected |
| Email | Resend or Gmail API | Transactional + scheduled |
| Deploy backend | Railway | Docker, auto-deploy, cheap |
| Deploy frontend | Vercel | Next.js native, edge, CDN |
| Workflows | n8n (self-hosted) | Flexible, AI agent nodes, cost-effective |
| AI Analysis | Claude Opus | Best reasoning for data analysis |
| AI Chat | Claude Sonnet | Fast enough for real-time Q&A |

### Security Checklist

- [ ] JWT auth with short-lived tokens (30min access, 7d refresh)
- [ ] Supabase RLS on ALL tables
- [ ] File upload validation (type, size, content)
- [ ] Rate limiting on analysis endpoint (expensive)
- [ ] Rate limiting on chat endpoint
- [ ] CORS restricted to frontend domain only
- [ ] API key management for enterprise tier
- [ ] Audit logging for data access
- [ ] GDPR: data deletion endpoint
- [ ] No PII in logs
