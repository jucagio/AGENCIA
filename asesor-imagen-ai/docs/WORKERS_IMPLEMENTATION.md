# Backend Workers Implementation (Sprint 0.5)

This document describes the implementation of the background background workers (ARQ) for the Asesor de Imagen AI backend, as well as instructions for maintaining and running them.

## Overview
The application uses **ARQ** (Async Redis Queue) to offload heavy or high-latency tasks such as AI model inferences and external API calls. This enables the FastAPI endpoints to return `202 Accepted` immediately (async-first paradigm, ADR-002).

There are three primary background workers:
1. **Vision Worker (`vision_worker.py`)**: Handles Google Cloud Vision API tasks and basic Claude analysis.
2. **Replicate Worker (`replicate_worker.py`)**: Handles Virtual Try-On inference using the Replicate API and Supabase Storage uploads.
3. **Claude Worker (`claude_worker.py`)**: Handles personalized outfit recommendation generation using Anthropic's Claude Opus model.

## Integrations

### 1. Google Cloud Vision API
Used for auto-tagging wardrobe items and analyzing body properties (skin tone, dominant colors).
- **Credentials**: Set `GOOGLE_CLOUD_VISION_API_KEY` in your `.env` file. Alternatively, standard GCP ADC (Application Default Credentials) via `GOOGLE_APPLICATION_CREDENTIALS` json works if deployed on GCP.
- **SSRF Protection**: Image URLs are strictly validated and limited to whitelisted domains (`supabase.co`, `storage.googleapis.com`, `replicate.com`, `example.com`).
- **Post-processing**: `vision_analyze_body` pipes the returned labels and colors to Claude to deduce `body_type` and `color_season`.

### 2. Replicate API
Used to run the Virtual Try-On image generation model.
- **Credentials**: Set `REPLICATE_API_TOKEN` in your `.env`.
- **Model Version**: Controlled by `REPLICATE_MODEL_VERSION` (defaults to `"replicate/replicate/tryon"`).
- **Rate Limiting**: The worker implements exponential backoff up to 3 retries specifically handling Replicate API `RateLimitError` or HTTP 429.
- **Storage**: The result image is downloaded and re-uploaded to Supabase Storage at `/try-ons/{user_id}/{try_on_id}.jpg`.

### 3. Anthropic (Claude) API
Used for intelligent outfit generation and style insights.
- **Credentials**: Set `ANTHROPIC_API_KEY` in your `.env`.
- **Model**: `claude-opus-4-7` is the default model.
- **Structured Output**: The worker specifically requests JSON and parses the response carefully to insert structured records into the `recommendation_items` table.

## Database & RLS
- The workers run **outside** the user request context. Therefore, they cannot rely on the standard user JWT to access Supabase.
- They use the `AdminClient` (using the service-role key) combined with the Cyber Neo H3 guard pattern: `admin.trusted().table("...").update(...)`.
- The `AdminClient` is injected into the ARQ context via `ctx.get("admin_client")`.

## Debugging Guidelines
- **Worker Logs**: Set the logging level to `DEBUG` in your environment. Look for `logger.info("process_try_on started: ...")`.
- **Redis Queue**: You can monitor jobs manually using `redis-cli`:
  ```bash
  redis-cli
  > keys arq:*
  ```
- **Error States**: If an external API fails repeatedly, the worker will update the relevant entity's status to `failed` and populate an error message where applicable, allowing the client to safely retry.

## Running Locally
To spin up the workers locally, use the arq CLI. Each worker module specifies a `WorkerSettings` class.
You can run them in parallel or sequentially.

```bash
# Terminal 1: Start the Replicate Worker
arq app.workers.replicate_worker.WorkerSettings

# Terminal 2: Start the Vision Worker
arq app.workers.vision_worker.WorkerSettings

# Terminal 3: Start the Claude Worker
arq app.workers.claude_worker.WorkerSettings
```
