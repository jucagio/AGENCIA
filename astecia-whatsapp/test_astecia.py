#!/usr/bin/env python3
"""
Test local de ASTECIA sin WhatsApp.
Útil para verificar que ASTECIA responde correctamente.

Uso:
    python test_astecia.py
"""

import os
import sys
from anthropic import Anthropic

# Sistema prompt de ASTECIA
ASTECIA_SYSTEM_PROMPT = """Eres ASTECIA, el asistente comercial estratégico de Juan Camilo Gil de MAPER S.A.

Combinas:
- LEO: vendedor que cierra deals con argumentos basados en valor
- YANG: investigadora que entiende el contexto de cada cliente
- JARVIS: estratega que piensa en ROI y portfolio

## Tu Rol
Responde preguntas comerciales de Juan Camilo en tiempo real:
- Análisis de oportunidades
- Investigación de empresas y decision makers
- Argumentarios de venta personalizados
- Estructuración de propuestas
- Manejo de objeciones
- Priorización del portfolio

## Reglas
1. Respuestas en ESPAÑOL únicamente
2. Máximo 200 palabras (WhatsApp-friendly)
3. Accionable hoy, no teoría
4. Sincero: di si algo no va a cerrar
5. Si necesitas más contexto, pregunta
6. Confidencial: todo entre tú y Juan Camilo

## Contexto MAPER S.A.
- Distribuidor exclusivo Videojet en Suroccidente Colombia (Valle, Cauca, Nariño)
- Equipos: CIJ, TTO, Laser, LCM, LPA
- Principales clientes: Cargill, Omnilife, Colombina, Tecnosur, Papeles del Cauca, Kimberly Clark

## Portfolio Actual (13-Abr-2026)
CRÍTICOS:
- POT 28546 (Cargill, 40M, negociación)
- POT 26108 (Omnilife, 52.2M, demo)
- POT 25641 (Colombina, 80M, cierre esperado)
- POT 27985 (Colombina, 126M, multi-equipo)
- KC-S2O (Kimberly Clark, 44eq, post-venta)

TIER 1 (80% feeling):
- Papeles del Cauca (168M, licitación)
- Belleza Express (48M+56M)
- O Tafur (180M, avícola)
- Tecnosur (36M, guerra competitiva)

Responde como lo haría Leo (vendedor), Yang (investigadora), o Jarvis (estratega) según la pregunta.
"""


def test_astecia():
    """Test interactivo de ASTECIA."""

    # Verificar API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY no configurada")
        print("Configura con: export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    # Inicializar cliente
    client = Anthropic(api_key=api_key)
    conversation_history = []

    print("=" * 70)
    print("ASTECIA TEST — Asistente Comercial de Juan Camilo Gil")
    print("=" * 70)
    print("Escribe tus preguntas. Escribe 'salir' para terminar.\n")

    # Test cases predefinidos
    test_questions = [
        "¿Vale la pena perseguir Prokpil?",
        "¿Quién es el decision maker real en Papeles del Cauca?",
        "Redacta un email de follow-up para Omnilife",
        "¿Cuál es mi mejor movimiento con Tecnosur?",
        "¿Cuánto vale cerrar Cargill vs el tiempo que le estoy invirtiendo?"
    ]

    print("Test automático con preguntas reales:\n")

    for i, question in enumerate(test_questions, 1):
        print(f"\n[Test {i}/{len(test_questions)}]")
        print(f"Pregunta: {question}")
        print("Respuesta: ", end="", flush=True)

        try:
            # Añadir a historial
            conversation_history.append({
                "role": "user",
                "content": question
            })

            # Invocar ASTECIA
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=500,
                system=ASTECIA_SYSTEM_PROMPT,
                messages=conversation_history
            )

            # Procesar respuesta
            answer = response.content[0].text
            conversation_history.append({
                "role": "assistant",
                "content": answer
            })

            print(answer)
            print("-" * 70)

        except Exception as e:
            print(f"ERROR: {str(e)}")
            sys.exit(1)

    # Conversación interactiva
    print("\n" + "=" * 70)
    print("Conversación interactiva (escribe 'salir' para terminar)")
    print("=" * 70)

    while True:
        user_input = input("\nTú: ").strip()

        if user_input.lower() == "salir":
            print("\nASTECIA: ¡Hasta luego! Recuerda: "
                  "cada call cuenta, cada email suma. ¡A cerrar deals!")
            break

        if not user_input:
            continue

        try:
            # Añadir a historial
            conversation_history.append({
                "role": "user",
                "content": user_input
            })

            # Invocar ASTECIA
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=500,
                system=ASTECIA_SYSTEM_PROMPT,
                messages=conversation_history
            )

            # Procesar respuesta
            answer = response.content[0].text
            conversation_history.append({
                "role": "assistant",
                "content": answer
            })

            print(f"\nASTECIA: {answer}")

        except Exception as e:
            print(f"ERROR: {str(e)}")
            break


if __name__ == "__main__":
    test_astecia()
