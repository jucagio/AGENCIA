#!/usr/bin/env python3
"""
Obsidian Bridge MCP Server — Integración de agentes con Obsidian vault.

Permite a los agentes:
- Leer notas del vault
- Escribir/crear notas automáticamente
- Crear ADRs (Architecture Decision Records)
- Actualizar progreso de proyectos
- Registrar decisiones críticas
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

# MCP Server base (usando server estándar sin dependencias externas)
class ObsidianBridge:
    """Bridge entre agentes y Obsidian vault."""

    def __init__(self, vault_path: str = "agencia-vault"):
        """Inicializa el bridge."""
        self.vault_path = Path(vault_path)
        self.metadata_path = self.vault_path / "06_Metadata"
        self.projects_path = self.vault_path / "01_Projects"
        self.areas_path = self.vault_path / "02_Areas"

        # Crear directorios si no existen
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Asegura que los directorios del vault existan."""
        dirs = [
            self.metadata_path / "Decisiones_ADR",
            self.metadata_path / "Auditorías",
            self.metadata_path / "Templates",
            self.projects_path,
            self.areas_path,
        ]

        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)

    # === LECTURA ===

    def read_note(self, path: str) -> Optional[str]:
        """
        Lee una nota del vault.

        Args:
            path: Ruta relativa al vault (ej: "01_Projects/Teclado_de_Senias/Proyecto.md")

        Returns:
            Contenido de la nota o None si no existe
        """
        note_path = self.vault_path / path
        if not note_path.exists():
            return None

        try:
            with open(note_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading {path}: {str(e)}"

    def get_agent_context(self, agent_name: str) -> Dict[str, Any]:
        """
        Obtiene contexto del agente (rol, instrucciones, estado actual).

        Args:
            agent_name: Nombre del agente (ej: "sasha", "jarvis")

        Returns:
            Dict con contexto del agente
        """
        try:
            # Buscar archivo de contexto del agente
            context_path = self.metadata_path / "Agentes" / f"{agent_name}.md"
            if context_path.exists():
                content = self.read_note(f"06_Metadata/Agentes/{agent_name}.md")
                return {
                    "agent": agent_name,
                    "context": content,
                    "found": True,
                }

            # Si no existe, retornar estructura vacía
            return {
                "agent": agent_name,
                "context": None,
                "found": False,
                "message": f"No context file for {agent_name}. Create at 06_Metadata/Agentes/{agent_name}.md",
            }
        except Exception as e:
            return {"error": str(e)}

    # === ESCRITURA ===

    def write_note(self, path: str, content: str, overwrite: bool = False) -> Dict[str, Any]:
        """
        Escribe/crea una nota en el vault.

        Args:
            path: Ruta relativa al vault
            content: Contenido de la nota
            overwrite: Si True, sobrescribe; si False, no sobrescribe

        Returns:
            Dict con resultado {"success": bool, "path": str, "message": str}
        """
        note_path = self.vault_path / path

        # Crear directorios padre si no existen
        note_path.parent.mkdir(parents=True, exist_ok=True)

        # Verificar si existe y no permitir sobrescritura
        if note_path.exists() and not overwrite:
            return {
                "success": False,
                "path": str(note_path),
                "message": f"Note already exists: {path}. Use overwrite=True to replace.",
            }

        try:
            with open(note_path, "w", encoding="utf-8") as f:
                f.write(content)

            return {
                "success": True,
                "path": str(note_path),
                "message": f"Note written: {path}",
                "size": len(content),
            }
        except Exception as e:
            return {
                "success": False,
                "path": str(note_path),
                "message": f"Error writing note: {str(e)}",
            }

    # === ADRs (Architecture Decision Records) ===

    def create_adr(
        self,
        title: str,
        context: str,
        decision: str,
        consequences: str,
        agent: str = "unknown",
    ) -> Dict[str, Any]:
        """
        Crea un Architecture Decision Record.

        Args:
            title: Título de la decisión
            context: Contexto y problema
            decision: Decisión tomada
            consequences: Consecuencias de la decisión
            agent: Agente que tomó la decisión

        Returns:
            Dict con resultado
        """
        # Encontrar número ADR siguiente
        adr_dir = self.metadata_path / "Decisiones_ADR"
        adr_dir.mkdir(parents=True, exist_ok=True)

        existing_adrs = list(adr_dir.glob("ADR-*.md"))
        next_number = len(existing_adrs) + 1

        # Crear contenido ADR
        adr_title = f"ADR-{next_number:03d}: {title}"
        adr_filename = f"ADR-{next_number:03d}-{title.replace(' ', '-').lower()}.md"

        adr_content = f"""# {adr_title}

**Agente:** {agent}
**Fecha:** {datetime.now().isoformat()}
**Status:** Accepted

## Context

{context}

## Decision

{decision}

## Consequences

### Positivas
- {consequences}

### Negativas
- (Por definir)

## Alternatives Considered

(Por definir)

---

*Creado automáticamente por {agent}*
"""

        return self.write_note(
            f"06_Metadata/Decisiones_ADR/{adr_filename}",
            adr_content,
            overwrite=False,
        )

    # === PROGRESO DE PROYECTOS ===

    def update_progress(
        self,
        project: str,
        status: str,
        metrics: Optional[Dict[str, Any]] = None,
        notes: str = "",
    ) -> Dict[str, Any]:
        """
        Actualiza el progreso de un proyecto.

        Args:
            project: Nombre del proyecto (ej: "Teclado_de_Senias")
            status: Estado (ej: "in_progress", "blocked", "complete")
            metrics: Dict con métricas (ej: {"completion": 75, "tasks_done": 15})
            notes: Notas adicionales

        Returns:
            Dict con resultado
        """
        progress_path = f"01_Projects/{project}/Progreso.md"
        existing = self.read_note(progress_path)

        # Crear o actualizar
        if existing:
            # Agregar al final del archivo
            update_entry = f"\n\n## Update — {datetime.now().isoformat()}\n"
            update_entry += f"**Status:** {status}\n"
            if metrics:
                update_entry += f"**Metrics:** {json.dumps(metrics)}\n"
            if notes:
                update_entry += f"**Notes:** {notes}\n"

            new_content = existing + update_entry
        else:
            # Crear nuevo archivo
            new_content = f"""# Progreso: {project}

## Update — {datetime.now().isoformat()}
**Status:** {status}
"""
            if metrics:
                new_content += f"**Metrics:** {json.dumps(metrics)}\n"
            if notes:
                new_content += f"**Notes:** {notes}\n"

        return self.write_note(progress_path, new_content, overwrite=True)

    # === LOGGING DE DECISIONES ===

    def log_decision(
        self,
        agent: str,
        decision: str,
        reasoning: str,
        impact: str = "medium",
    ) -> Dict[str, Any]:
        """
        Registra una decisión crítica.

        Args:
            agent: Nombre del agente
            decision: La decisión tomada
            reasoning: Razonamiento detrás
            impact: Impacto ("low", "medium", "high")

        Returns:
            Dict con resultado
        """
        log_path = f"06_Metadata/Auditorías/{agent}_decisions.md"
        existing = self.read_note(log_path)

        entry = f"""## {datetime.now().isoformat()} — {decision}

**Agent:** {agent}
**Impact:** {impact}

### Reasoning
{reasoning}

---
"""

        if existing:
            new_content = existing + "\n" + entry
        else:
            new_content = f"""# Decisiones — {agent}

{entry}"""

        return self.write_note(log_path, new_content, overwrite=True)

    # === UTILIDADES ===

    def list_notes(self, path: str = "") -> List[str]:
        """
        Lista todas las notas en un directorio.

        Args:
            path: Ruta relativa al vault

        Returns:
            Lista de rutas de notas
        """
        search_path = self.vault_path / path
        if not search_path.exists():
            return []

        notes = []
        for md_file in search_path.rglob("*.md"):
            relative = md_file.relative_to(self.vault_path)
            notes.append(str(relative))

        return sorted(notes)

    def get_vault_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del vault."""
        all_notes = self.list_notes()
        return {
            "vault_path": str(self.vault_path),
            "total_notes": len(all_notes),
            "exists": self.vault_path.exists(),
            "last_update": datetime.now().isoformat(),
        }


# === CLI INTERFACE ===

def main():
    """CLI para testing del MCP server."""
    import sys

    bridge = ObsidianBridge()

    # Ejemplo 1: Listar notas
    print("[LIST] Notas en el vault:")
    notes = bridge.list_notes("01_Projects")
    for note in notes[:5]:
        print(f"  - {note}")

    # Ejemplo 2: Estadísticas
    stats = bridge.get_vault_stats()
    print(f"\n[STATS] Estadísticas: {stats['total_notes']} notas")

    # Ejemplo 3: Crear ADR
    print("\n[CREATE] Creando ADR de ejemplo...")
    result = bridge.create_adr(
        title="Usar Obsidian para persistencia de agentes",
        context="Necesitamos persistencia de estado sin bases de datos complejas",
        decision="Usamos Obsidian vault + JSON en .agent-state/ para persistencia",
        consequences="Simplificamos infraestructura, todo versionado en Git",
        agent="jarvis",
    )
    print(f"  Resultado: {result['message']}")

    # Ejemplo 4: Actualizar progreso
    print("\n[UPDATE] Actualizando progreso...")
    result = bridge.update_progress(
        project="Teclado_de_Senias",
        status="in_progress",
        metrics={"phase": "FASE_3_MCP", "completion": 33},
        notes="MCP server implementado",
    )
    print(f"  Resultado: {result['message']}")

    # Ejemplo 5: Log de decisión
    print("\n[LOG] Registrando decisión...")
    result = bridge.log_decision(
        agent="jarvis",
        decision="Implementar MCP server para Obsidian",
        reasoning="Permite automatización de decisiones y auditoría en vault",
        impact="high",
    )
    print(f"  Resultado: {result['message']}")

    print("\n[OK] MCP Server funcional")


if __name__ == "__main__":
    main()
