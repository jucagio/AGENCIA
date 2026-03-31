-- =============================================================================
-- MAPER.IA — Schema de Supabase
-- Bot asesor industrial para MAPERSA en Facebook Messenger
-- Orquestado por n8n + Claude Sonnet 4.6
--
-- Ejecutar en: Supabase SQL Editor (completo, en orden)
-- =============================================================================

-- ---------------------------------------------------------------------------
-- 0. LIMPIEZA (DROP si ya existen — seguro para re-ejecutar)
-- ---------------------------------------------------------------------------
DROP TABLE IF EXISTS public.escalations   CASCADE;
DROP TABLE IF EXISTS public.follow_ups    CASCADE;
DROP TABLE IF EXISTS public.leads         CASCADE;
DROP TABLE IF EXISTS public.messages      CASCADE;
DROP TABLE IF EXISTS public.conversations CASCADE;
DROP TABLE IF EXISTS public.contacts      CASCADE;

DROP TYPE IF EXISTS escalation_status;
DROP TYPE IF EXISTS follow_up_status;
DROP TYPE IF EXISTS lead_status;
DROP TYPE IF EXISTS message_role;

-- ---------------------------------------------------------------------------
-- 1. EXTENSIONES
-- ---------------------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS "pgcrypto";  -- Para gen_random_uuid() si no esta activa

-- ---------------------------------------------------------------------------
-- 2. TIPOS ENUMERADOS
-- ---------------------------------------------------------------------------

-- Rol del mensaje en la conversacion
CREATE TYPE message_role AS ENUM ('user', 'assistant', 'system');

-- Estado del lead comercial
CREATE TYPE lead_status AS ENUM ('cold', 'warm', 'hot', 'won', 'lost');

-- Estado del seguimiento programado
CREATE TYPE follow_up_status AS ENUM ('pending', 'completed', 'cancelled');

-- Estado del escalamiento
CREATE TYPE escalation_status AS ENUM ('open', 'in_progress', 'resolved', 'closed');

-- ---------------------------------------------------------------------------
-- 2. FUNCION AUXILIAR: updated_at automatico
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ---------------------------------------------------------------------------
-- 3. TABLA: contacts
-- Clientes y prospectos que escriben por Messenger
-- ---------------------------------------------------------------------------
CREATE TABLE public.contacts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    messenger_sender_id TEXT NOT NULL UNIQUE,
        -- ID unico del usuario en Facebook Messenger (PSID)
    name            TEXT,
        -- Nombre del contacto (puede venir del perfil de FB o ser capturado en la conversacion)
    phone           TEXT,
        -- Telefono capturado durante la conversacion
    email           TEXT,
        -- Email capturado durante la conversacion
    company         TEXT,
        -- Empresa del contacto (relevante para ventas industriales)
    industry        TEXT,
        -- Sector industrial (codificacion, inspeccion, maquinaria, etc.)
    metadata        JSONB DEFAULT '{}',
        -- Datos adicionales flexibles: cargo, ubicacion, productos de interes, etc.
    first_message_at TIMESTAMPTZ,
        -- Cuando nos escribio por primera vez
    last_message_at  TIMESTAMPTZ,
        -- Ultimo mensaje recibido (se actualiza con cada interaccion)
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.contacts IS 'Clientes y prospectos que interactuan con el bot de MAPERSA por Messenger';
COMMENT ON COLUMN public.contacts.messenger_sender_id IS 'Page-Scoped ID (PSID) del usuario en Facebook Messenger — unico por pagina';
COMMENT ON COLUMN public.contacts.metadata IS 'Datos flexibles: cargo, ubicacion, productos de interes, notas del bot';

CREATE TRIGGER trg_contacts_updated_at
    BEFORE UPDATE ON public.contacts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ---------------------------------------------------------------------------
-- 4. TABLA: conversations
-- Sesiones de conversacion agrupadas por contacto
-- ---------------------------------------------------------------------------
CREATE TABLE public.conversations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id      UUID NOT NULL REFERENCES public.contacts(id) ON DELETE CASCADE,
    started_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
        -- Cuando inicio esta sesion de conversacion
    ended_at        TIMESTAMPTZ,
        -- Cuando se cerro (NULL = activa)
    summary         TEXT,
        -- Resumen generado por el AI al cerrar la conversacion
    topic           TEXT,
        -- Tema principal detectado: cotizacion, soporte, informacion, etc.
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.conversations IS 'Sesiones de conversacion — agrupa mensajes por interaccion logica con un contacto';
COMMENT ON COLUMN public.conversations.summary IS 'Resumen generado por IA al cerrar la conversacion — util para contexto futuro';

CREATE TRIGGER trg_conversations_updated_at
    BEFORE UPDATE ON public.conversations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ---------------------------------------------------------------------------
-- 5. TABLA: messages
-- Mensajes individuales (entrada del usuario y respuesta del bot)
-- ---------------------------------------------------------------------------
CREATE TABLE public.messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES public.conversations(id) ON DELETE CASCADE,
    contact_id      UUID NOT NULL REFERENCES public.contacts(id) ON DELETE CASCADE,
        -- Denormalizado desde conversation para queries directas por contacto
    role            message_role NOT NULL,
        -- 'user' = mensaje del cliente, 'assistant' = respuesta del bot, 'system' = nota interna
    content         TEXT NOT NULL,
        -- Contenido del mensaje
    metadata        JSONB DEFAULT '{}',
        -- Datos extra: intent detectado, confidence score, attachments, etc.
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.messages IS 'Mensajes individuales — historial completo para alimentar la memoria del AI Agent';
COMMENT ON COLUMN public.messages.role IS 'user = cliente, assistant = bot, system = nota interna del sistema';
COMMENT ON COLUMN public.messages.contact_id IS 'Denormalizado para queries directas por contacto sin JOIN a conversations';

-- No necesita updated_at — los mensajes son inmutables una vez creados

-- ---------------------------------------------------------------------------
-- 6. TABLA: leads
-- Oportunidades comerciales detectadas por el bot
-- ---------------------------------------------------------------------------
CREATE TABLE public.leads (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id      UUID NOT NULL REFERENCES public.contacts(id) ON DELETE CASCADE,
    status          lead_status NOT NULL DEFAULT 'cold',
        -- cold → warm → hot → won/lost
    estimated_value NUMERIC(12, 2),
        -- Valor estimado de la oportunidad en COP/USD
    currency        TEXT DEFAULT 'COP',
    product_interest TEXT[],
        -- Array de productos/servicios de interes: {'codificadoras', 'bandas_transportadoras', etc.}
    notes           TEXT,
        -- Notas del bot o del asesor humano sobre esta oportunidad
    qualified_at    TIMESTAMPTZ,
        -- Cuando el bot califico este lead como warm/hot
    won_at          TIMESTAMPTZ,
        -- Cuando se cerro como ganado
    lost_at         TIMESTAMPTZ,
        -- Cuando se cerro como perdido
    lost_reason     TEXT,
        -- Razon de perdida (si aplica)
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.leads IS 'Oportunidades comerciales — el bot detecta y califica leads automaticamente';
COMMENT ON COLUMN public.leads.product_interest IS 'Array de productos MAPERSA: codificadoras, bandas, detectores_metal, etc.';
COMMENT ON COLUMN public.leads.status IS 'Embudo: cold (nuevo) → warm (interesado) → hot (listo para comprar) → won/lost';

CREATE TRIGGER trg_leads_updated_at
    BEFORE UPDATE ON public.leads
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ---------------------------------------------------------------------------
-- 7. TABLA: follow_ups
-- Seguimientos programados por el bot o el asesor
-- ---------------------------------------------------------------------------
CREATE TABLE public.follow_ups (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id      UUID NOT NULL REFERENCES public.contacts(id) ON DELETE CASCADE,
    lead_id         UUID REFERENCES public.leads(id) ON DELETE SET NULL,
        -- Opcional: vinculado a un lead especifico
    scheduled_at    TIMESTAMPTZ NOT NULL,
        -- Cuando debe ejecutarse el seguimiento
    reason          TEXT NOT NULL,
        -- Motivo del seguimiento: "enviar cotizacion", "verificar recepcion", etc.
    message_template TEXT,
        -- Mensaje sugerido para el seguimiento (el bot puede personalizarlo)
    status          follow_up_status NOT NULL DEFAULT 'pending',
    completed_at    TIMESTAMPTZ,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.follow_ups IS 'Seguimientos programados — n8n los consulta periodicamente para ejecutarlos';
COMMENT ON COLUMN public.follow_ups.scheduled_at IS 'n8n ejecuta un cron que busca follow_ups con scheduled_at <= NOW() y status = pending';

CREATE TRIGGER trg_follow_ups_updated_at
    BEFORE UPDATE ON public.follow_ups
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ---------------------------------------------------------------------------
-- 8. TABLA: escalations
-- Casos escalados al asesor humano
-- ---------------------------------------------------------------------------
CREATE TABLE public.escalations (
    id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    contact_id          UUID NOT NULL REFERENCES public.contacts(id) ON DELETE CASCADE,
    reason              TEXT NOT NULL,
        -- Motivo del escalamiento: "solicita hablar con humano", "pregunta fuera de alcance", etc.
    conversation_snippet TEXT,
        -- Ultimos mensajes relevantes para que el asesor tenga contexto rapido
    status              escalation_status NOT NULL DEFAULT 'open',
    assigned_to         TEXT,
        -- Nombre o ID del asesor humano asignado
    resolved_at         TIMESTAMPTZ,
    resolution_notes    TEXT,
        -- Notas del asesor humano al resolver
    metadata            JSONB DEFAULT '{}',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMENT ON TABLE public.escalations IS 'Casos que el bot escala al equipo humano de MAPERSA';
COMMENT ON COLUMN public.escalations.conversation_snippet IS 'Ultimos 5-10 mensajes como contexto rapido para el asesor humano';

CREATE TRIGGER trg_escalations_updated_at
    BEFORE UPDATE ON public.escalations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ---------------------------------------------------------------------------
-- 9. INDICES
-- Optimizados para las queries que n8n ejecuta frecuentemente
-- ---------------------------------------------------------------------------

-- contacts: busqueda por sender_id (ya tiene UNIQUE, que crea indice)
-- No se necesita indice adicional en messenger_sender_id

-- conversations: buscar conversaciones activas de un contacto
CREATE INDEX idx_conversations_contact_id ON public.conversations(contact_id);
CREATE INDEX idx_conversations_contact_active ON public.conversations(contact_id)
    WHERE ended_at IS NULL;
    -- Indice parcial: solo conversaciones activas (las mas consultadas)

-- messages: historial por contacto ordenado por tiempo (query principal del bot)
CREATE INDEX idx_messages_contact_id_created ON public.messages(contact_id, created_at DESC);
-- messages: buscar por conversacion
CREATE INDEX idx_messages_conversation_id ON public.messages(conversation_id);

-- leads: buscar por contacto y por estado
CREATE INDEX idx_leads_contact_id ON public.leads(contact_id);
CREATE INDEX idx_leads_status ON public.leads(status);
CREATE INDEX idx_leads_contact_status ON public.leads(contact_id, status);

-- follow_ups: el cron de n8n busca seguimientos pendientes
CREATE INDEX idx_follow_ups_pending ON public.follow_ups(scheduled_at)
    WHERE status = 'pending';
    -- Indice parcial: solo pendientes (lo que el cron necesita)
CREATE INDEX idx_follow_ups_contact_id ON public.follow_ups(contact_id);

-- escalations: casos abiertos
CREATE INDEX idx_escalations_open ON public.escalations(created_at DESC)
    WHERE status = 'open';
CREATE INDEX idx_escalations_contact_id ON public.escalations(contact_id);

-- ---------------------------------------------------------------------------
-- 10. ROW LEVEL SECURITY (RLS)
-- Solo el service_role (n8n) puede leer y escribir.
-- El anon key y authenticated users NO tienen acceso.
-- ---------------------------------------------------------------------------

ALTER TABLE public.contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.follow_ups ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.escalations ENABLE ROW LEVEL SECURITY;

-- NOTA IMPORTANTE:
-- El service_role key de Supabase BYPASEA RLS automaticamente.
-- Por lo tanto, n8n (que usa service_role) puede leer/escribir sin policies.
-- No creamos policies para anon ni authenticated porque NO deben tener acceso.
-- Si en el futuro se necesita un dashboard web, se agregan policies especificas.

-- Politica explicita: denegar todo acceso a roles no-service
-- (RLS habilitado sin policies = acceso denegado por defecto para anon/authenticated)

-- Si se necesita un dashboard futuro con auth de Supabase, agregar:
-- CREATE POLICY "Admins read contacts" ON public.contacts
--     FOR SELECT TO authenticated
--     USING ((auth.jwt()->>'user_role') = 'admin');

-- ---------------------------------------------------------------------------
-- 11. REALTIME (opcional — habilitar si se necesita dashboard en vivo)
-- ---------------------------------------------------------------------------
-- Descomentar si se implementa un dashboard que necesite actualizaciones en vivo:
-- ALTER PUBLICATION supabase_realtime ADD TABLE public.messages;
-- ALTER PUBLICATION supabase_realtime ADD TABLE public.leads;
-- ALTER PUBLICATION supabase_realtime ADD TABLE public.escalations;

-- =============================================================================
-- FIN DEL SCHEMA
-- =============================================================================
