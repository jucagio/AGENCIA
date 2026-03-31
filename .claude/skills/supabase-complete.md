# Supabase Complete — Skill para Claude Code

## Descripcion
Skill experta en Supabase que cubre Auth, Row Level Security (RLS), Realtime, Edge Functions, Storage y PostgreSQL avanzado. Va mas alla de las mejores practicas genericas de Postgres para cubrir el ecosistema completo de Supabase. Optimizada para Sasha y Brook.

## Instrucciones

Cuando el usuario pida ayuda con Supabase, sigue estas directrices:

### Auth — Autenticacion y Autorizacion

**Flujos de autenticacion soportados:**

| Metodo | Caso de uso | Implementacion |
|--------|-------------|----------------|
| Email/Password | Apps con registro propio | `supabase.auth.signUp()` / `signInWithPassword()` |
| Magic Link | Login sin password | `supabase.auth.signInWithOtp({ email })` |
| OAuth | Login con Google, GitHub, etc. | `supabase.auth.signInWithOAuth({ provider })` |
| Phone OTP | Verificacion por SMS | `supabase.auth.signInWithOtp({ phone })` |
| Anonymous | Usuarios temporales | `supabase.auth.signInAnonymously()` |

**Configuracion de Auth en Dashboard:**
1. Authentication > Providers > Habilitar los necesarios
2. Authentication > URL Configuration > Site URL + Redirect URLs
3. Authentication > Email Templates > Personalizar emails de confirmacion

**JWT y roles:**
- Supabase genera JWT automaticamente al login
- El JWT contiene: `sub` (user id), `role` (authenticated/anon), `email`, custom claims
- El token se pasa automaticamente en requests al API REST
- Para agregar claims personalizados (ej: admin role):

```sql
-- Crear funcion que agrega claims al JWT
CREATE OR REPLACE FUNCTION public.custom_access_token_hook(event jsonb)
RETURNS jsonb LANGUAGE plpgsql AS $$
DECLARE
  claims jsonb;
  user_role text;
BEGIN
  SELECT role INTO user_role FROM public.user_profiles WHERE id = (event->>'user_id')::uuid;

  claims := event->'claims';
  claims := jsonb_set(claims, '{user_role}', to_jsonb(user_role));
  event := jsonb_set(event, '{claims}', claims);

  RETURN event;
END;
$$;
```

### Row Level Security (RLS) — Patrones Avanzados

**Regla fundamental:** SIEMPRE habilitar RLS en TODAS las tablas. Sin RLS, cualquier usuario con el anon key puede leer/escribir todo.

```sql
-- Habilitar RLS
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;

-- Patron 1: El usuario solo ve sus propios registros
CREATE POLICY "Users see own orders"
ON public.orders FOR SELECT
TO authenticated
USING (user_id = auth.uid());

-- Patron 2: El usuario crea registros asociados a si mismo
CREATE POLICY "Users create own orders"
ON public.orders FOR INSERT
TO authenticated
WITH CHECK (user_id = auth.uid());

-- Patron 3: El usuario solo edita sus propios registros
CREATE POLICY "Users update own orders"
ON public.orders FOR UPDATE
TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());

-- Patron 4: Admins ven todo (usando custom claim)
CREATE POLICY "Admins see all orders"
ON public.orders FOR SELECT
TO authenticated
USING (
  (auth.jwt()->>'user_role') = 'admin'
);

-- Patron 5: Acceso basado en organizacion/equipo
CREATE POLICY "Team members see team orders"
ON public.orders FOR SELECT
TO authenticated
USING (
  team_id IN (
    SELECT team_id FROM public.team_members
    WHERE user_id = auth.uid()
  )
);

-- Patron 6: Registros publicos + privados
CREATE POLICY "Public or own items"
ON public.items FOR SELECT
TO authenticated
USING (
  is_public = true
  OR user_id = auth.uid()
);
```

**Errores comunes de RLS:**
- Olvidar `USING` vs `WITH CHECK`: USING filtra lectura, WITH CHECK valida escritura
- No indexar las columnas usadas en policies (ej: `user_id`, `team_id`)
- Policies recursivas: una policy en tabla A que consulta tabla B que tiene policy consultando tabla A
- Service role key bypasea RLS — NUNCA exponerla al frontend

### Realtime — Suscripciones en Tiempo Real

```typescript
// Flutter (supabase_flutter)
final channel = supabase.channel('orders');
channel.onPostgresChanges(
  event: PostgresChangeEvent.all,
  schema: 'public',
  table: 'orders',
  filter: PostgresChangeFilter(
    type: PostgresChangeFilterType.eq,
    column: 'user_id',
    value: supabase.auth.currentUser!.id,
  ),
  callback: (payload) {
    print('Change: ${payload.eventType} - ${payload.newRecord}');
  },
).subscribe();

// JavaScript/TypeScript
const channel = supabase
  .channel('orders')
  .on('postgres_changes',
    { event: '*', schema: 'public', table: 'orders', filter: `user_id=eq.${userId}` },
    (payload) => console.log('Change:', payload)
  )
  .subscribe();
```

**Habilitar Realtime en una tabla:**
```sql
ALTER PUBLICATION supabase_realtime ADD TABLE public.orders;
```

**Broadcast (para mensajes efimeros, no persisten en BD):**
```typescript
const channel = supabase.channel('room-1');
channel.on('broadcast', { event: 'cursor-pos' }, (payload) => {
  console.log('Cursor:', payload);
});
channel.subscribe((status) => {
  if (status === 'SUBSCRIBED') {
    channel.send({ type: 'broadcast', event: 'cursor-pos', payload: { x: 100, y: 200 } });
  }
});
```

### Edge Functions

```typescript
// supabase/functions/hello/index.ts
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

serve(async (req) => {
  // CORS headers
  if (req.method === "OPTIONS") {
    return new Response("ok", {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST",
        "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
      },
    });
  }

  try {
    // Auth: obtener usuario del JWT
    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_ANON_KEY")!,
      { global: { headers: { Authorization: req.headers.get("Authorization")! } } }
    );
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) throw new Error("Unauthorized");

    const { name } = await req.json();
    return new Response(JSON.stringify({ message: `Hello ${name}!` }), {
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }
});
```

**Deploy:**
```bash
supabase functions deploy hello
supabase functions serve hello  # Local testing
```

### Storage

```typescript
// Subir archivo
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`${userId}/avatar.png`, file, {
    cacheControl: '3600',
    upsert: true,
    contentType: 'image/png',
  });

// URL publica
const { data: { publicUrl } } = supabase.storage
  .from('avatars')
  .getPublicUrl(`${userId}/avatar.png`);

// URL firmada (temporal, para archivos privados)
const { data: { signedUrl } } = await supabase.storage
  .from('documents')
  .createSignedUrl(`${userId}/contract.pdf`, 3600); // 1 hora
```

**Storage Policies (similar a RLS):**
```sql
-- Usuarios suben a su propia carpeta
CREATE POLICY "Users upload own avatars"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'avatars' AND (storage.foldername(name))[1] = auth.uid()::text);

-- Avatares son publicos para lectura
CREATE POLICY "Avatars are publicly accessible"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'avatars');
```

### PostgreSQL Avanzado en Supabase

**Indices para performance:**
```sql
-- Indice en columnas usadas en WHERE y RLS policies
CREATE INDEX idx_orders_user_id ON public.orders(user_id);
CREATE INDEX idx_orders_status ON public.orders(status);
CREATE INDEX idx_orders_created_at ON public.orders(created_at DESC);

-- Indice compuesto para queries frecuentes
CREATE INDEX idx_orders_user_status ON public.orders(user_id, status);

-- Indice parcial (solo indexa filas que cumplen condicion)
CREATE INDEX idx_active_orders ON public.orders(user_id) WHERE status = 'active';

-- Full-text search
ALTER TABLE public.products ADD COLUMN fts tsvector
  GENERATED ALWAYS AS (to_tsvector('spanish', coalesce(name, '') || ' ' || coalesce(description, ''))) STORED;
CREATE INDEX idx_products_fts ON public.products USING gin(fts);
```

**Database Functions (para logica compleja en el servidor):**
```sql
CREATE OR REPLACE FUNCTION public.get_dashboard_stats(p_user_id uuid)
RETURNS jsonb LANGUAGE plpgsql SECURITY DEFINER AS $$
DECLARE
  result jsonb;
BEGIN
  SELECT jsonb_build_object(
    'total_orders', (SELECT count(*) FROM orders WHERE user_id = p_user_id),
    'total_revenue', (SELECT coalesce(sum(total), 0) FROM orders WHERE user_id = p_user_id AND status = 'completed'),
    'pending_orders', (SELECT count(*) FROM orders WHERE user_id = p_user_id AND status = 'pending')
  ) INTO result;

  RETURN result;
END;
$$;
```

**Llamar funciones desde el cliente:**
```typescript
const { data } = await supabase.rpc('get_dashboard_stats', { p_user_id: userId });
```

### Migraciones

```bash
# Crear migracion
supabase migration new create_orders_table

# Aplicar migraciones locales
supabase db reset

# Push a produccion
supabase db push

# Pull schema de produccion
supabase db pull
```

### Mejores Practicas

1. **RLS siempre activo** en todas las tablas. Sin excepciones.
2. **Anon key en frontend, service_role en backend.** Nunca al reves.
3. **Indices en columnas de RLS policies.** Sin indice, cada policy hace full table scan.
4. **Edge Functions para logica sensible.** No confiar solo en RLS para reglas de negocio complejas.
5. **Migraciones versionadas.** Usar `supabase migration` para todo cambio de schema.
6. **Backups automaticos.** Supabase Pro hace backups diarios. Verificar que esten activos.
7. **Connection pooling.** Usar el connection string de Supavisor (puerto 6543) para aplicaciones con muchas conexiones.
8. **Monitorear queries lentas.** Dashboard > Database > Query Performance.
9. **Separar schemas.** Usar schema `public` para datos de la app, nunca modificar `auth` o `storage` directamente.
10. **Typed clients.** Generar tipos con `supabase gen types typescript` para autocompletado en el frontend.
