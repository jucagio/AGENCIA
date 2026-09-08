<#
.SYNOPSIS
  Aplica las migraciones SQL de producción a un proyecto Supabase real.

.DESCRIPTION
  Sprint Fase 1 — Supabase Real. Owner: Sasha.

  Aplica EN ORDEN sobre una base de datos Supabase vacía:
    1. 004_consolidated_schema_v2.sql    (schema base 12 tablas, ADR-001)
    2. 002_storage_buckets.sql           (buckets + storage RLS)
    3. 005_rls_policies.sql              (RLS user-scoped)
    4. 006_rate_limit_rpc.sql            (rate limit RPC atómico)
    5. 007_optionf_fsm_cache_tier.sql    (FSM + cache tier + lazy reset)
    6. 008_tighten_try_ons_update.sql    (Cyber Neo FIX 1)

  Es IDEMPOTENTE: si corre 2 veces consecutivas, no falla.

  Opcionalmente crea usuarios de prueba en auth.users + public.profiles.

.PARAMETER DbUrl
  Connection string PostgreSQL de Supabase.
  Formato: postgresql://postgres.[REF]:[PASSWORD]@aws-X-region.pooler.supabase.com:6543/postgres
  Obtener en: Supabase Dashboard > Project Settings > Database > Connection string > URI.

.PARAMETER SeedTestUsers
  Si se pasa, crea 2 usuarios de prueba: test1@asesor.ai / Test1234!, test2@asesor.ai / Test1234!.
  Requiere SUPABASE_URL + SUPABASE_SERVICE_ROLE_KEY en .env (los lee).

.PARAMETER DryRun
  Solo lista las migraciones a aplicar, no ejecuta nada.

.EXAMPLE
  .\apply_migrations.ps1 -DbUrl "postgresql://postgres.xxx:pwd@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

.EXAMPLE
  .\apply_migrations.ps1 -DbUrl $env:SUPABASE_DB_URL -SeedTestUsers

.NOTES
  Requiere `psql` instalado y en PATH. En Windows:
    winget install PostgreSQL.PostgreSQL.16
  O usar el cliente que viene con Supabase CLI:
    https://supabase.com/docs/guides/cli
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, HelpMessage = "Supabase DB connection string (postgresql://...)")]
    [string]$DbUrl,

    [switch]$SeedTestUsers,

    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

# ---------------------------------------------------------------------------
# Migration order (PRODUCTION fresh-start path)
# ---------------------------------------------------------------------------
$migrations = @(
    '004_consolidated_schema_v2.sql',
    '002_storage_buckets.sql',
    '005_rls_policies.sql',
    '006_rate_limit_rpc.sql',
    '007_optionf_fsm_cache_tier.sql',
    '008_tighten_try_ons_update.sql'
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$migrationsDir = Join-Path $scriptDir 'migrations'

# ---------------------------------------------------------------------------
# Pre-flight checks
# ---------------------------------------------------------------------------
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  Sprint Fase 1 — Apply Supabase Migrations" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verify psql
$psql = (Get-Command psql -ErrorAction SilentlyContinue).Source
if (-not $psql) {
    Write-Host "[ERROR] psql not found in PATH." -ForegroundColor Red
    Write-Host "Install with: winget install PostgreSQL.PostgreSQL.16" -ForegroundColor Yellow
    exit 1
}
Write-Host "[OK] psql found: $psql" -ForegroundColor Green

# Verify migrations directory
if (-not (Test-Path $migrationsDir)) {
    Write-Host "[ERROR] Migrations directory not found: $migrationsDir" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Migrations dir: $migrationsDir" -ForegroundColor Green

# Verify all migration files exist
foreach ($m in $migrations) {
    $path = Join-Path $migrationsDir $m
    if (-not (Test-Path $path)) {
        Write-Host "[ERROR] Missing migration file: $path" -ForegroundColor Red
        exit 1
    }
}
Write-Host "[OK] All 6 migration files present." -ForegroundColor Green

# Mask DbUrl for logs (hide password)
$dbUrlSafe = $DbUrl -replace '(:)([^:@]+)(@)', '$1***$3'
Write-Host "[OK] DB URL: $dbUrlSafe" -ForegroundColor Green

if ($DryRun) {
    Write-Host ""
    Write-Host "[DRY RUN] Migrations that would be applied (in order):" -ForegroundColor Yellow
    $i = 1
    foreach ($m in $migrations) {
        Write-Host "  $i. $m" -ForegroundColor Yellow
        $i++
    }
    Write-Host ""
    Write-Host "Re-run without -DryRun to execute." -ForegroundColor Yellow
    exit 0
}

# ---------------------------------------------------------------------------
# Connectivity test
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "[1/3] Testing connection to Supabase..." -ForegroundColor Cyan
$testQuery = "SELECT current_database(), current_user, version();"
$testOut = & psql $DbUrl -t -c $testQuery 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to connect:" -ForegroundColor Red
    Write-Host $testOut -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Connected." -ForegroundColor Green
Write-Host "      $($testOut -join ' ' | ForEach-Object { $_.Trim() })" -ForegroundColor Gray

# ---------------------------------------------------------------------------
# Apply migrations in order
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "[2/3] Applying migrations..." -ForegroundColor Cyan

$applied = 0
$failed = @()
foreach ($m in $migrations) {
    $path = Join-Path $migrationsDir $m
    Write-Host ""
    Write-Host "  -> Applying $m ..." -ForegroundColor Yellow
    & psql $DbUrl -v ON_ERROR_STOP=1 -f $path
    if ($LASTEXITCODE -eq 0) {
        Write-Host "     [OK] $m applied." -ForegroundColor Green
        $applied++
    } else {
        Write-Host "     [FAIL] $m" -ForegroundColor Red
        $failed += $m
    }
}

Write-Host ""
Write-Host "[2/3] Migrations summary: $applied applied, $($failed.Count) failed." -ForegroundColor Cyan
if ($failed.Count -gt 0) {
    Write-Host "Failed migrations:" -ForegroundColor Red
    $failed | ForEach-Object { Write-Host "  - $_" -ForegroundColor Red }
    exit 1
}

# ---------------------------------------------------------------------------
# Post-apply verification
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "[3/3] Post-apply verification..." -ForegroundColor Cyan

$verifyTables = @"
SELECT count(*) FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN (
    'profiles', 'subscriptions', 'wardrobe_items', 'body_analysis',
    'try_ons', 'try_on_cache', 'recommendations', 'recommendation_items',
    'user_style_profile', 'usage_counters', 'idempotency_keys', 'audit_log'
  );
"@
$tableCount = (& psql $DbUrl -t -c $verifyTables).Trim()
Write-Host "  Tables present: $tableCount / 12" -ForegroundColor $(if ($tableCount -eq '12') { 'Green' } else { 'Red' })

$verifyPolicies = "SELECT count(*) FROM pg_policies WHERE schemaname = 'public';"
$policyCount = (& psql $DbUrl -t -c $verifyPolicies).Trim()
Write-Host "  RLS policies: $policyCount (expect >=24)" -ForegroundColor $(if ([int]$policyCount -ge 24) { 'Green' } else { 'Red' })

$verifyBuckets = "SELECT count(*) FROM storage.buckets WHERE id IN ('avatars', 'wardrobe', 'tryons');"
$bucketCount = (& psql $DbUrl -t -c $verifyBuckets).Trim()
Write-Host "  Storage buckets: $bucketCount / 3" -ForegroundColor $(if ($bucketCount -eq '3') { 'Green' } else { 'Red' })

$verifyTighten = "SELECT count(*) FROM pg_policy WHERE polrelid = 'public.try_ons'::regclass AND polname = 'try_ons_update_service_role_only';"
$tightenCount = (& psql $DbUrl -t -c $verifyTighten).Trim()
Write-Host "  try_ons UPDATE locked (FIX 1): $(if ($tightenCount -eq '1') { 'YES' } else { 'NO' })" -ForegroundColor $(if ($tightenCount -eq '1') { 'Green' } else { 'Red' })

# ---------------------------------------------------------------------------
# Optional: Seed test users
# ---------------------------------------------------------------------------
if ($SeedTestUsers) {
    Write-Host ""
    Write-Host "[BONUS] Seeding test users via Supabase Admin API..." -ForegroundColor Cyan

    # Read .env for SUPABASE_URL + SERVICE_ROLE_KEY
    $envFile = Join-Path $scriptDir '.env'
    if (-not (Test-Path $envFile)) {
        Write-Host "  [SKIP] .env not found; cannot create users without SUPABASE_URL/SERVICE_ROLE_KEY." -ForegroundColor Yellow
    } else {
        $envVars = @{}
        Get-Content $envFile | ForEach-Object {
            if ($_ -match '^\s*([A-Z_]+)\s*=\s*(.*)\s*$') {
                $envVars[$Matches[1]] = $Matches[2]
            }
        }
        $supaUrl = $envVars['SUPABASE_URL']
        $serviceKey = $envVars['SUPABASE_SERVICE_ROLE_KEY']

        if (-not $supaUrl -or -not $serviceKey) {
            Write-Host "  [SKIP] SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY missing in .env." -ForegroundColor Yellow
        } else {
            $testUsers = @(
                @{ email = 'test1@asesor.ai'; password = 'Test1234!' },
                @{ email = 'test2@asesor.ai'; password = 'Test1234!' }
            )
            foreach ($u in $testUsers) {
                $body = @{
                    email = $u.email
                    password = $u.password
                    email_confirm = $true
                } | ConvertTo-Json
                $headers = @{
                    'apikey' = $serviceKey
                    'Authorization' = "Bearer $serviceKey"
                    'Content-Type' = 'application/json'
                }
                try {
                    $resp = Invoke-RestMethod -Uri "$supaUrl/auth/v1/admin/users" -Method POST -Headers $headers -Body $body -ErrorAction Stop
                    Write-Host "  [OK] Created user: $($u.email) (id=$($resp.id))" -ForegroundColor Green
                } catch {
                    # 422 = email already exists; treat as idempotent success
                    if ($_.Exception.Response.StatusCode.value__ -eq 422) {
                        Write-Host "  [SKIP] User $($u.email) already exists." -ForegroundColor Yellow
                    } else {
                        Write-Host "  [FAIL] Could not create $($u.email): $($_.Exception.Message)" -ForegroundColor Red
                    }
                }
            }
        }
    }
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "  DONE. Migrations applied successfully." -ForegroundColor Green
Write-Host "  Next: run .\verify_supabase_ready.py" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
