---
name: postgres-best-practices
description: >
  Mejores prácticas de PostgreSQL y Supabase: diseño de esquemas, índices, RLS,
  consultas optimizadas, migraciones y performance. Usar cuando se diseñe el esquema
  de base de datos, se optimicen consultas lentas, se configure Row Level Security
  en Supabase, o se planifiquen migraciones. Agentes: Sasha, Brook.
---

# PostgreSQL & Supabase — Best Practices

## Diseño de Esquemas

### Convenciones de nomenclatura

```sql
-- Tablas: snake_case plural
CREATE TABLE users (...);
CREATE TABLE order_items (...);

-- Columnas: snake_case
user_id, created_at, is_active

-- Índices: idx_tabla_columna
CREATE INDEX idx_users_email ON users(email);

-- Foreign keys: tabla_id
user_id REFERENCES users(id)
```

### Campos obligatorios en cada tabla

```sql
CREATE TABLE users (
    id          UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    created_at  TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    updated_at  TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    deleted_at  TIMESTAMPTZ,  -- soft delete

    -- campos propios
    email       TEXT NOT NULL UNIQUE,
    full_name   TEXT NOT NULL
);

-- Trigger para updated_at automático
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
```

### UUIDs vs Auto-increment

```sql
-- ✅ UUID para recursos expuestos en URLs (seguridad + escalabilidad)
id UUID DEFAULT gen_random_uuid() PRIMARY KEY

-- ✅ BIGSERIAL para tablas internas con muchos inserts (logs, events)
id BIGSERIAL PRIMARY KEY
```

---

## Índices — Cuándo y cómo

### Índices que SIEMPRE debes crear

```sql
-- Foreign keys (Postgres NO los crea automáticamente)
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);

-- Campos de búsqueda frecuente
CREATE INDEX idx_users_email ON users(email);

-- Campos de ordenamiento en listados
CREATE INDEX idx_orders_created_at ON orders(created_at DESC);

-- Soft delete: filtrar activos es muy común
CREATE INDEX idx_users_active ON users(id) WHERE deleted_at IS NULL;
```

### Índices compuestos (para queries específicas)

```sql
-- Si buscas frecuentemente por: WHERE user_id = X AND status = 'active' ORDER BY created_at
CREATE INDEX idx_orders_user_status_created
ON orders(user_id, status, created_at DESC);
```

### Verificar índices inutilizados

```sql
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0  -- nunca usado
ORDER BY pg_relation_size(indexrelid) DESC;
```

---

## Row Level Security (RLS) en Supabase

### Habilitar RLS (obligatorio en Supabase)

```sql
-- Habilitar RLS en todas las tablas que contienen datos de usuarios
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
```

### Políticas básicas

```sql
-- SELECT: usuario solo ve sus propios datos
CREATE POLICY "users_select_own_orders"
ON orders FOR SELECT
USING (auth.uid() = user_id);

-- INSERT: usuario solo puede crear para sí mismo
CREATE POLICY "users_insert_own_orders"
ON orders FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- UPDATE: usuario solo modifica sus propios datos
CREATE POLICY "users_update_own_orders"
ON orders FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);

-- DELETE (soft delete recomendado)
CREATE POLICY "users_soft_delete_own_orders"
ON orders FOR UPDATE
USING (auth.uid() = user_id);
```

### Política para admins

```sql
-- Admins ven todo
CREATE POLICY "admins_full_access"
ON orders FOR ALL
USING (
    EXISTS (
        SELECT 1 FROM user_roles
        WHERE user_id = auth.uid() AND role = 'admin'
    )
);
```

---

## Queries Optimizadas

### Evitar N+1 queries

```sql
-- ❌ MAL: N+1 (1 query por user + N queries por orders)
-- SELECT * FROM users
-- Para cada usuario: SELECT * FROM orders WHERE user_id = ?

-- ✅ BIEN: JOIN o window functions
SELECT
    u.id, u.email, u.full_name,
    COUNT(o.id) as order_count,
    SUM(o.total) as total_spent
FROM users u
LEFT JOIN orders o ON o.user_id = u.id AND o.deleted_at IS NULL
WHERE u.deleted_at IS NULL
GROUP BY u.id, u.email, u.full_name
ORDER BY u.created_at DESC
LIMIT 20 OFFSET 0;
```

### Paginación eficiente (cursor vs offset)

```sql
-- ❌ OFFSET lento en tablas grandes (escanea todas las filas anteriores)
SELECT * FROM orders ORDER BY created_at DESC LIMIT 20 OFFSET 1000;

-- ✅ CURSOR (keyset pagination) — O(log n) siempre
SELECT * FROM orders
WHERE created_at < '2026-03-01T00:00:00Z'  -- cursor del último item
ORDER BY created_at DESC
LIMIT 20;
```

### EXPLAIN ANALYZE — diagnosticar queries lentas

```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM orders
WHERE user_id = 'uuid-here' AND status = 'pending'
ORDER BY created_at DESC;

-- Buscar en el output:
-- "Seq Scan" → falta un índice
-- "cost" alto → optimizar la query
-- "actual time" vs "estimated" → estadísticas desactualizadas → ANALYZE
```

---

## Migraciones

### Reglas de migraciones seguras en producción

```sql
-- ✅ Agregar columna nullable (no bloquea tabla)
ALTER TABLE users ADD COLUMN phone TEXT;

-- ✅ Agregar columna con DEFAULT (desde Postgres 11)
ALTER TABLE users ADD COLUMN is_verified BOOLEAN DEFAULT false;

-- ⚠️ Agregar NOT NULL constraint — hacerlo en 3 pasos:
-- Paso 1: agregar nullable
ALTER TABLE users ADD COLUMN preferences JSONB;
-- Paso 2: backfill con datos
UPDATE users SET preferences = '{}' WHERE preferences IS NULL;
-- Paso 3: agregar constraint
ALTER TABLE users ALTER COLUMN preferences SET NOT NULL;

-- ❌ NUNCA hacer en producción sin análisis:
-- DROP TABLE, DROP COLUMN (data loss)
-- ALTER COLUMN TYPE en tablas grandes (bloquea la tabla)
-- ADD CONSTRAINT sin validación de datos existentes
```

---

## Performance — Checklist

```sql
-- 1. Estadísticas actualizadas
ANALYZE users;
ANALYZE orders;

-- 2. Vacuum para recuperar espacio
VACUUM ANALYZE orders;

-- 3. Tablas con más bloat
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;

-- 4. Queries más lentas
SELECT query, calls, total_exec_time/calls as avg_ms, rows/calls as avg_rows
FROM pg_stat_statements
ORDER BY avg_ms DESC
LIMIT 10;
```

---

## Checklist de entrega (Sasha verifica antes de entregar a Brook)

```
[ ] Todas las tablas tienen id (UUID), created_at, updated_at
[ ] Tablas con datos de usuario tienen deleted_at (soft delete)
[ ] Foreign keys tienen índices
[ ] Campos de búsqueda frecuente tienen índices
[ ] RLS habilitado en todas las tablas de usuarios (Supabase)
[ ] Políticas RLS cubren SELECT, INSERT, UPDATE, DELETE
[ ] Migraciones son reversibles (tiene rollback)
[ ] Ninguna migración bloquea tablas en producción
[ ] EXPLAIN ANALYZE en queries complejas (sin Seq Scan en tablas grandes)
```

*Fuente: VoltAgent/Supabase Postgres Best Practices Skill + PostgreSQL Official Docs*
