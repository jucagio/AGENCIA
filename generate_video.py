#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador automático de video "El Fin del Desperdicio"
Café Águila Roja + Videojet 7920 UV Laser
Usa Higgsfield MCP API para generar clips en paralelo
"""

import os
import json
import time
import sys
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Fix UTF-8 en Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

API_KEY_ID = os.getenv("HIGGSFIELD_API_KEY_ID")
API_KEY_SECRET = os.getenv("HIGGSFIELD_API_KEY_SECRET")

if not API_KEY_ID or not API_KEY_SECRET:
    raise ValueError("Faltan credenciales. Revisa .claude/settings.local.json: HIGGSFIELD_API_KEY_ID y HIGGSFIELD_API_KEY_SECRET")

OUTPUT_DIR = Path("./videos_output")
OUTPUT_DIR.mkdir(exist_ok=True)

HIGGSFIELD_API_URL = "https://api.higgsfield.ai/v1"
MODEL = "sora"  # Sora 2 es el modelo base
RESOLUTION = "1080p"
ASPECT_RATIO = "16:9"

# ============================================================================
# DEFINICIÓN DE CLIPS
# ============================================================================

CLIPS = [
    {
        "id": "clip_1",
        "name": "01_Dolor_Financiero",
        "duration": 15,
        "visual_prompt": """Granino, mascota amarilla y roja con cara sonriente, vestido de ejecutivo en traje formal gris,
mirando una MONTAÑA GIGANTE de empaques de café rotos, perforados y desperdiciados.
El Granino tiene expresión de preocupación y dolor. Suelo lleno de café derramado.
Cámara zoom lento hacia la montaña de desperdicio. Escala cinescópica épica.
Iluminación industrial cálida, atmósfera corporativa seria. Colores: amarillo+rojo (Granino),
tonos cafés, grises corporativos. Estilo: motion graphics realista + 3D.""",
        "voice_script": "¿Cuánto te cuesta la fricción física? Cada empaque perforado por el Hot Stamp son 50 COP directos a la basura.",
        "music_mood": "corporate_dramatic_low"
    },
    {
        "id": "clip_2",
        "name": "02_Falsa_Promesa",
        "duration": 25,
        "visual_prompt": """Close-up técnico profesional de cabezal TTO (Thermal Transfer Overprinting) industrial sucio,
lleno de polvo café oscuro y aceite. Zoom progresivo macro que muestra polvo bloqueando ribbon
de transferencia. Colores oscuros: negros, grises, rojos industriales. Iluminación técnica dura.
Código impreso ilegible visible a lado (borroso, ilegible). Timestamp visible en pantalla.
Cámara inspección de calidad industrial. Transición suave a siguiente plano.""",
        "voice_script": "Intentaste evolucionar al TTO, pero el polvillo y los aceites del café bloquean la adherencia del ribbon. Códigos borrosos, pérdida de trazabilidad y paradas de línea constantes.",
        "music_mood": "industrial_tense"
    },
    {
        "id": "clip_3",
        "name": "03_Ataque_Tecnologico",
        "duration": 35,
        "visual_prompt": """Rayo láser UV azul brillante e impecable escaneando bolsa de café Águila Roja en movimiento.
Marcaje perfecto sin contacto físico, indeleble. Fondo oscuro. Código resultante NÍTIDO 100% legible.
Cámara sigue movimiento del láser en tiempo real. Efectos de luz: reflejo azul intenso,
humo ligero de marcado, partículas de energía. El Granino reaparece sonriendo en esquina inferior.
Transición dinámica. Estilo: sci-fi industrial, premium. Paleta: azul + blanco (láser),
rojo+amarillo (Granino), café natural.""",
        "voice_script": "El cambio de paradigma llegó. Videojet 7920 Láser UV. Marcaje 100% sin contacto. Nuestra tecnología SmartFocus™ ajusta automáticamente la distancia focal, absorbiendo las variaciones de la bolsa de café sin intervención del operario.",
        "music_mood": "ascending_technology"
    },
    {
        "id": "clip_4",
        "name": "04_Golpe_Gracia",
        "duration": 35,
        "visual_prompt": """Gráficos dinámicos ASCENDENTES que muestran $250K COP/día, $18M COP recuperados, $9,200 USD anuales,
OEE 68% → 94%. Fondo azul corporativo oscuro. El Granino aparece cargando una bolsa gigante de dinero.
Animación de crecimiento exponencial fluido. Números grandes y legibles (60pt+).
SFX visual: monedas cayendo, calculadora, checkmarks verdes. Transición suave hacia clip final.
Estilo: fintech moderno, premium, confiable.""",
        "voice_script": "Pasa de un gasto variable a una eficiencia fija. Erradica la compra de consumibles y ahorra $9,200 USD anuales. Recupera el OEE de tu planta.",
        "music_mood": "ascending_victory"
    },
    {
        "id": "clip_5",
        "name": "05_Cierre_Directo",
        "duration": 10,
        "visual_prompt": """ESCENA 1: Logo MAPER aparece (fade-in). Juan Camilo rostro profesional, confiado.
ESCENA 2: Fundido a línea de empaque de Café Águila Roja funcionando PERFECTAMENTE.
Código láser PERFECTO. Operarios sonrientes. El Granino thumbs-up.
TEXT: cafeaguilaroja.com/videojet7920 / 48h Demo GRATIS / MAPER logo""",
        "voice_script": "Trazabilidad absoluta e indeleble. Protege la marca Águila Roja. Agenda tu prueba de concepto con MAPER hoy. El tiempo de inactividad te está costando dinero.",
        "music_mood": "triumph_final"
    }
]

# ============================================================================
# FUNCIONES
# ============================================================================

def generate_video_clip(clip: dict) -> dict:
    """Genera un clip de video usando Higgsfield API"""
    clip_id = clip["id"]
    print(f"\n🎬 Generando {clip_id} ({clip['duration']}s)...")

    try:
        # Preparar payload para Higgsfield API
        payload = {
            "prompt": clip["visual_prompt"],
            "model": MODEL,
            "duration": clip["duration"],
            "aspect_ratio": ASPECT_RATIO,
            "resolution": RESOLUTION,
            "style": "cinematic"
        }

        # Headers con autenticación (Basic Auth)
        import base64
        credentials = base64.b64encode(f"{API_KEY_ID}:{API_KEY_SECRET}".encode()).decode()
        headers = {
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/json"
        }

        # Llamar API Higgsfield
        response = requests.post(
            f"{HIGGSFIELD_API_URL}/generate/video",
            json=payload,
            headers=headers,
            timeout=300
        )

        if response.status_code != 200:
            raise Exception(f"API error: {response.status_code} - {response.text}")

        result = response.json()
        video_url = result.get("video_url")

        if not video_url:
            raise Exception("No video URL in response")

        # Descargar el video
        print(f"   ✓ Video generado. Descargando...")
        video_response = requests.get(video_url, timeout=120)

        if video_response.status_code != 200:
            raise Exception(f"Download failed: {video_response.status_code}")

        # Guardar archivo
        output_path = OUTPUT_DIR / f"{clip['name']}.mp4"
        with open(output_path, "wb") as f:
            f.write(video_response.content)

        file_size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"   ✓ {clip['name']}.mp4 guardado ({file_size_mb:.1f}MB)")

        return {
            "clip_id": clip_id,
            "name": clip["name"],
            "path": str(output_path),
            "status": "success",
            "duration": clip["duration"],
            "voice_script": clip["voice_script"]
        }

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return {
            "clip_id": clip_id,
            "name": clip["name"],
            "status": "failed",
            "error": str(e)
        }

def generate_all_clips() -> list:
    """Genera todos los clips en paralelo"""
    print("=" * 70)
    print("🚀 INICIANDO GENERACIÓN DE VIDEO (5 CLIPS EN PARALELO)")
    print("=" * 70)
    print(f"API Key ID: {'*' * 20}...{API_KEY_ID[-4:]}")
    print(f"Output: {OUTPUT_DIR.absolute()}")
    print(f"Total duración: {sum(c['duration'] for c in CLIPS)}s")

    results = []

    # Ejecutar generación en paralelo (max 3 simultáneamente)
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(generate_video_clip, clip): clip for clip in CLIPS}

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

    return results

def generate_compilation_script(results: list) -> str:
    """Genera script de edición para DaVinci Resolve / Premiere Pro"""

    successful_clips = [r for r in results if r["status"] == "success"]

    script = f"""
# ============================================================================
# SCRIPT DE COMPILACIÓN — El Fin del Desperdicio
# ============================================================================
# Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# Total clips: {len(successful_clips)}/{len(CLIPS)}
# Duración: {sum(c['duration'] for c in CLIPS)}s

## PASOS EN DAVINCI RESOLVE O PREMIERE PRO:

1. **Crear nuevo proyecto:**
   - Resolución: 1920x1080 (1080p)
   - Frame rate: 30fps
   - Aspect ratio: 16:9

2. **Importar clips en ORDEN:**
"""

    for i, result in enumerate(sorted(successful_clips, key=lambda x: x["clip_id"]), 1):
        script += f"\n   {i}. {result['path']}"

    script += """

3. **Agregar audio en timeline:**
   - PISTA 1: Voz en off (sincronizada)
   - PISTA 2: Música de fondo (baja)
   - PISTA 3: SFX (puntuales)

4. **Scripts de voz en off (copiar en orden):**
"""

    for result in sorted(successful_clips, key=lambda x: x["clip_id"]):
        script += f"\n   [{result['name']}] {result['voice_script']}"

    script += """

5. **Color grading uniforme:**
   - Aplicar LUT: Alexa LogC (o similar corporativo)
   - Saturación: +15%
   - Contrast: +10%
   - Temperatura: Neutral (4500K)

6. **Transiciones:**
   - Entre clips: Dip to Black (0.3s)
   - Dentro del clip 5: Fade (0.5s)

7. **Render final:**
   - Formato: H.264 MP4
   - Bitrate: 6000 kbps
   - Resolución: 1920x1080
   - Frame rate: 30fps

8. **Subtítulos (opcional):**
   - Idioma: Español
   - Formato: SRT
   - Posición: Abajo
"""

    return script

def main():
    """Función principal"""
    try:
        # Generar clips
        results = generate_all_clips()

        # Reporte
        print("\n" + "=" * 70)
        print("📊 REPORTE FINAL")
        print("=" * 70)

        success_count = sum(1 for r in results if r["status"] == "success")
        failed_count = sum(1 for r in results if r["status"] == "failed")

        print(f"\nExito: {success_count}/{len(CLIPS)}")
        print(f"Fallos: {failed_count}/{len(CLIPS)}")

        if failed_count > 0:
            print("\nClips fallidos:")
            for r in results:
                if r["status"] == "failed":
                    print(f"  - {r['name']}: {r.get('error', 'Unknown error')}")

        # Generar script de compilación
        if success_count > 0:
            script = generate_compilation_script(results)
            script_path = OUTPUT_DIR / "COMPILACION_SCRIPT.md"
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(script)

            print(f"\n📝 Script de compilación: {script_path}")

        # Resumen final
        print("\n" + "=" * 70)
        print("🎬 PRÓXIMOS PASOS:")
        print("=" * 70)

        if success_count == len(CLIPS):
            print("✅ Todos los clips generados exitosamente.")
            print("\n1. Abre DaVinci Resolve o Premiere Pro")
            print("2. Sigue el script: COMPILACION_SCRIPT.md")
            print("3. Importa clips en orden")
            print("4. Agrega voz en off + música")
            print("5. Render final: H.264 MP4 1080p")
            print(f"\n📁 Clips en: {OUTPUT_DIR.absolute()}")
        else:
            print(f"⚠️  {failed_count} clip(s) fallaron. Revisa arriba.")
            print(f"📁 Clips parciales en: {OUTPUT_DIR.absolute()}")

        print("\n" + "=" * 70)
        print("¡Video listo para edición!\n")

    except Exception as e:
        print(f"\n❌ Error fatal: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
