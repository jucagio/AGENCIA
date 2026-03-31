-- =============================================================================
-- MAPER.IA — Funciones SQL de utilidad para n8n
-- Diseñadas para ser llamadas desde n8n via supabase.rpc()
--
-- Ejecutar DESPUES de supabase-schema.sql
-- =============================================================================

-- ---------------------------------------------------------------------------
-- 1. get_or_create_contact(sender_id, name)
-- Crea el contacto si no existe, lo devuelve si ya existe.
-- n8n llama esto al inicio de cada interaccion.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.get_or_create_contact(
    p_sender_id TEXT,
    p_name TEXT DEFAULT NULL
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER  -- Se ejecuta con permisos del owner (bypasea RLS)
AS $$
DECLARE
    v_contact RECORD;
    v_now TIMESTAMPTZ := NOW();
BEGIN
    -- Intentar encontrar el contacto existente
    SELECT * INTO v_contact
    FROM public.contacts
    WHERE messenger_sender_id = p_sender_id;

    IF FOUND THEN
        -- Contacto existe: actualizar last_message_at y nombre si viene uno nuevo
        UPDATE public.contacts
        SET
            last_message_at = v_now,
            name = COALESCE(p_name, contacts.name)
        WHERE id = v_contact.id
        RETURNING * INTO v_contact;
    ELSE
        -- Contacto nuevo: crear
        INSERT INTO public.contacts (
            messenger_sender_id,
            name,
            first_message_at,
            last_message_at
        ) VALUES (
            p_sender_id,
            p_name,
            v_now,
            v_now
        )
        RETURNING * INTO v_contact;
    END IF;

    RETURN to_jsonb(v_contact);
END;
$$;

COMMENT ON FUNCTION public.get_or_create_contact IS
    'Busca un contacto por sender_id. Si no existe, lo crea. Retorna el contacto como JSON.';

-- ---------------------------------------------------------------------------
-- 2. get_conversation_history(sender_id, limit)
-- Retorna los ultimos N mensajes de un contacto para alimentar el contexto
-- del AI Agent. Ordenados de mas antiguo a mas reciente.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.get_conversation_history(
    p_sender_id TEXT,
    p_limit INT DEFAULT 20
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
STABLE  -- No modifica datos, puede optimizarse
AS $$
DECLARE
    v_contact_id UUID;
    v_messages JSONB;
BEGIN
    -- Obtener el contact_id
    SELECT id INTO v_contact_id
    FROM public.contacts
    WHERE messenger_sender_id = p_sender_id;

    IF NOT FOUND THEN
        RETURN '[]'::JSONB;
    END IF;

    -- Obtener ultimos N mensajes ordenados cronologicamente
    -- Subconsulta con DESC + LIMIT para tomar los ultimos N,
    -- luego wrapper con ASC para que el AI los reciba en orden correcto
    SELECT COALESCE(jsonb_agg(
        jsonb_build_object(
            'role', sub.role,
            'content', sub.content,
            'created_at', sub.created_at,
            'metadata', sub.metadata
        )
    ), '[]'::JSONB)
    INTO v_messages
    FROM (
        SELECT role::TEXT, content, created_at, metadata
        FROM public.messages
        WHERE contact_id = v_contact_id
        ORDER BY created_at DESC
        LIMIT p_limit
    ) sub
    ORDER BY sub.created_at ASC;

    RETURN v_messages;
END;
$$;

COMMENT ON FUNCTION public.get_conversation_history IS
    'Retorna los ultimos N mensajes de un contacto como array JSON, ordenados cronologicamente. Usa sender_id como entrada.';

-- ---------------------------------------------------------------------------
-- 3. save_message(sender_id, role, content, metadata)
-- Guarda un mensaje en el historial. Crea conversacion activa si no existe.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.save_message(
    p_sender_id TEXT,
    p_role TEXT,
    p_content TEXT,
    p_metadata JSONB DEFAULT '{}'
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_contact_id UUID;
    v_conversation_id UUID;
    v_message RECORD;
    v_role message_role;
BEGIN
    -- Validar el role
    BEGIN
        v_role := p_role::message_role;
    EXCEPTION WHEN invalid_text_representation THEN
        RAISE EXCEPTION 'Role invalido: %. Debe ser user, assistant o system.', p_role;
    END;

    -- Obtener contact_id
    SELECT id INTO v_contact_id
    FROM public.contacts
    WHERE messenger_sender_id = p_sender_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contacto no encontrado para sender_id: %. Usa get_or_create_contact primero.', p_sender_id;
    END IF;

    -- Buscar conversacion activa (sin ended_at)
    SELECT id INTO v_conversation_id
    FROM public.conversations
    WHERE contact_id = v_contact_id
      AND ended_at IS NULL
    ORDER BY created_at DESC
    LIMIT 1;

    -- Si no hay conversacion activa, crear una
    IF v_conversation_id IS NULL THEN
        INSERT INTO public.conversations (contact_id, started_at)
        VALUES (v_contact_id, NOW())
        RETURNING id INTO v_conversation_id;
    END IF;

    -- Insertar el mensaje
    INSERT INTO public.messages (
        conversation_id,
        contact_id,
        role,
        content,
        metadata
    ) VALUES (
        v_conversation_id,
        v_contact_id,
        v_role,
        p_content,
        p_metadata
    )
    RETURNING * INTO v_message;

    -- Actualizar last_message_at en el contacto
    UPDATE public.contacts
    SET last_message_at = NOW()
    WHERE id = v_contact_id;

    RETURN to_jsonb(v_message);
END;
$$;

COMMENT ON FUNCTION public.save_message IS
    'Guarda un mensaje en el historial. Crea conversacion activa automaticamente si no existe.';

-- ---------------------------------------------------------------------------
-- 4. create_or_update_lead(sender_id, status, notes, estimated_value,
--    product_interest)
-- Gestiona el estado del lead. Si el contacto ya tiene un lead activo
-- (no won/lost), lo actualiza. Si no, crea uno nuevo.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.create_or_update_lead(
    p_sender_id TEXT,
    p_status TEXT DEFAULT 'cold',
    p_notes TEXT DEFAULT NULL,
    p_estimated_value NUMERIC DEFAULT NULL,
    p_product_interest TEXT[] DEFAULT NULL
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_contact_id UUID;
    v_lead RECORD;
    v_status lead_status;
    v_now TIMESTAMPTZ := NOW();
BEGIN
    -- Validar status
    BEGIN
        v_status := p_status::lead_status;
    EXCEPTION WHEN invalid_text_representation THEN
        RAISE EXCEPTION 'Status invalido: %. Debe ser cold, warm, hot, won o lost.', p_status;
    END;

    -- Obtener contact_id
    SELECT id INTO v_contact_id
    FROM public.contacts
    WHERE messenger_sender_id = p_sender_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contacto no encontrado para sender_id: %. Usa get_or_create_contact primero.', p_sender_id;
    END IF;

    -- Buscar lead activo (no cerrado: ni won ni lost)
    SELECT * INTO v_lead
    FROM public.leads
    WHERE contact_id = v_contact_id
      AND status NOT IN ('won', 'lost')
    ORDER BY created_at DESC
    LIMIT 1;

    IF FOUND THEN
        -- Actualizar lead existente
        UPDATE public.leads
        SET
            status = v_status,
            notes = COALESCE(p_notes, leads.notes),
            estimated_value = COALESCE(p_estimated_value, leads.estimated_value),
            product_interest = COALESCE(p_product_interest, leads.product_interest),
            qualified_at = CASE
                WHEN v_status IN ('warm', 'hot') AND leads.qualified_at IS NULL THEN v_now
                ELSE leads.qualified_at
            END,
            won_at = CASE WHEN v_status = 'won' THEN v_now ELSE NULL END,
            lost_at = CASE WHEN v_status = 'lost' THEN v_now ELSE NULL END,
            lost_reason = CASE WHEN v_status = 'lost' THEN p_notes ELSE NULL END
        WHERE id = v_lead.id
        RETURNING * INTO v_lead;
    ELSE
        -- Crear nuevo lead
        INSERT INTO public.leads (
            contact_id,
            status,
            notes,
            estimated_value,
            product_interest,
            qualified_at
        ) VALUES (
            v_contact_id,
            v_status,
            p_notes,
            p_estimated_value,
            p_product_interest,
            CASE WHEN v_status IN ('warm', 'hot') THEN v_now ELSE NULL END
        )
        RETURNING * INTO v_lead;
    END IF;

    RETURN to_jsonb(v_lead);
END;
$$;

COMMENT ON FUNCTION public.create_or_update_lead IS
    'Crea o actualiza un lead activo para un contacto. Si el lead actual esta cerrado (won/lost), crea uno nuevo.';

-- ---------------------------------------------------------------------------
-- 5. create_escalation(sender_id, reason, conversation_snippet)
-- Registra un escalamiento al equipo humano.
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.create_escalation(
    p_sender_id TEXT,
    p_reason TEXT,
    p_conversation_snippet TEXT DEFAULT NULL
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_contact_id UUID;
    v_snippet TEXT;
    v_escalation RECORD;
BEGIN
    -- Obtener contact_id
    SELECT id INTO v_contact_id
    FROM public.contacts
    WHERE messenger_sender_id = p_sender_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contacto no encontrado para sender_id: %. Usa get_or_create_contact primero.', p_sender_id;
    END IF;

    -- Si no viene snippet, generar uno automaticamente con los ultimos 5 mensajes
    IF p_conversation_snippet IS NULL THEN
        SELECT string_agg(
            role::TEXT || ': ' || content,
            E'\n'
            ORDER BY created_at ASC
        )
        INTO v_snippet
        FROM (
            SELECT role, content, created_at
            FROM public.messages
            WHERE contact_id = v_contact_id
            ORDER BY created_at DESC
            LIMIT 5
        ) sub;
    ELSE
        v_snippet := p_conversation_snippet;
    END IF;

    -- Crear el escalamiento
    INSERT INTO public.escalations (
        contact_id,
        reason,
        conversation_snippet,
        status
    ) VALUES (
        v_contact_id,
        p_reason,
        v_snippet,
        'open'
    )
    RETURNING * INTO v_escalation;

    RETURN to_jsonb(v_escalation);
END;
$$;

COMMENT ON FUNCTION public.create_escalation IS
    'Registra un caso escalado al equipo humano. Si no se pasa snippet, lo genera automaticamente con los ultimos 5 mensajes.';

-- ---------------------------------------------------------------------------
-- 6. FUNCIONES AUXILIARES ADICIONALES (utiles para n8n)
-- ---------------------------------------------------------------------------

-- 6a. Obtener follow-ups pendientes que ya vencieron (para el cron de n8n)
CREATE OR REPLACE FUNCTION public.get_pending_follow_ups()
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
STABLE
AS $$
DECLARE
    v_result JSONB;
BEGIN
    SELECT COALESCE(jsonb_agg(
        jsonb_build_object(
            'follow_up_id', fu.id,
            'contact_id', fu.contact_id,
            'sender_id', c.messenger_sender_id,
            'contact_name', c.name,
            'reason', fu.reason,
            'message_template', fu.message_template,
            'scheduled_at', fu.scheduled_at,
            'lead_id', fu.lead_id
        )
    ), '[]'::JSONB)
    INTO v_result
    FROM public.follow_ups fu
    JOIN public.contacts c ON c.id = fu.contact_id
    WHERE fu.status = 'pending'
      AND fu.scheduled_at <= NOW()
    ORDER BY fu.scheduled_at ASC;

    RETURN v_result;
END;
$$;

COMMENT ON FUNCTION public.get_pending_follow_ups IS
    'Retorna follow-ups pendientes que ya pasaron su hora programada. El cron de n8n llama esto cada X minutos.';

-- 6b. Marcar un follow-up como completado
CREATE OR REPLACE FUNCTION public.complete_follow_up(
    p_follow_up_id UUID
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_follow_up RECORD;
BEGIN
    UPDATE public.follow_ups
    SET
        status = 'completed',
        completed_at = NOW()
    WHERE id = p_follow_up_id
      AND status = 'pending'
    RETURNING * INTO v_follow_up;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Follow-up no encontrado o ya no esta pendiente: %', p_follow_up_id;
    END IF;

    RETURN to_jsonb(v_follow_up);
END;
$$;

COMMENT ON FUNCTION public.complete_follow_up IS
    'Marca un follow-up como completado. Solo funciona si el follow-up esta en estado pending.';

-- 6c. Crear un follow-up programado
CREATE OR REPLACE FUNCTION public.schedule_follow_up(
    p_sender_id TEXT,
    p_reason TEXT,
    p_scheduled_at TIMESTAMPTZ,
    p_message_template TEXT DEFAULT NULL,
    p_lead_id UUID DEFAULT NULL
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_contact_id UUID;
    v_follow_up RECORD;
BEGIN
    -- Obtener contact_id
    SELECT id INTO v_contact_id
    FROM public.contacts
    WHERE messenger_sender_id = p_sender_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Contacto no encontrado para sender_id: %', p_sender_id;
    END IF;

    INSERT INTO public.follow_ups (
        contact_id,
        lead_id,
        scheduled_at,
        reason,
        message_template,
        status
    ) VALUES (
        v_contact_id,
        p_lead_id,
        p_scheduled_at,
        p_reason,
        p_message_template,
        'pending'
    )
    RETURNING * INTO v_follow_up;

    RETURN to_jsonb(v_follow_up);
END;
$$;

COMMENT ON FUNCTION public.schedule_follow_up IS
    'Programa un seguimiento futuro para un contacto. n8n lo ejecutara cuando llegue la hora.';

-- 6d. Obtener escalamientos abiertos (para notificar al equipo humano)
CREATE OR REPLACE FUNCTION public.get_open_escalations()
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
STABLE
AS $$
DECLARE
    v_result JSONB;
BEGIN
    SELECT COALESCE(jsonb_agg(
        jsonb_build_object(
            'escalation_id', e.id,
            'contact_id', e.contact_id,
            'sender_id', c.messenger_sender_id,
            'contact_name', c.name,
            'reason', e.reason,
            'conversation_snippet', e.conversation_snippet,
            'created_at', e.created_at
        )
    ), '[]'::JSONB)
    INTO v_result
    FROM public.escalations e
    JOIN public.contacts c ON c.id = e.contact_id
    WHERE e.status = 'open'
    ORDER BY e.created_at ASC;

    RETURN v_result;
END;
$$;

COMMENT ON FUNCTION public.get_open_escalations IS
    'Retorna escalamientos abiertos con datos del contacto. Util para el dashboard o notificaciones.';

-- =============================================================================
-- FIN DE FUNCIONES
-- =============================================================================
