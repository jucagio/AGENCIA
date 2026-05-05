# Computer Use Basics — Claude API Computer Control

## Descripcion
Skill para entender y usar Claude Computer Use API (beta). Permite a Claude controlar mouse, teclado y pantalla para automatizar tareas de RPA, testing y workflows no estructurados. Optimizada para Sasha (research) y Alejo (architecture decisions).

## Instrucciones

Cuando el usuario pregunte sobre Computer Use, RPA con Claude, o automatizacion de desktop, sigue estas directrices:

### Que es Computer Use

Computer Use es una capacidad beta de la Claude API que permite a Claude:
- **Ver la pantalla** via screenshots
- **Mover el mouse** y hacer click
- **Escribir texto** via teclado
- **Ejecutar comandos** de bash
- **Editar archivos** con un text editor tool

Es un loop continuo: screenshot → analizar → decidir accion → ejecutar → screenshot → repetir.

### Estado Actual (Abril 2026)

| Aspecto | Status |
|---------|--------|
| API disponible | Si, beta |
| Beta header requerido | `computer-use-2025-11-24` |
| Modelos soportados | Claude Opus 4.6, Sonnet 4.6, Opus 4.5 |
| Plataformas | Linux (nativo), macOS (parcial), Windows (limitado) |
| Latencia por accion | 2-5 segundos promedio |
| Zoom action | Disponible con `enable_zoom: true` |
| Produccion-ready | NO — beta, no recomendado para flujos criticos |

### Setup Basico

```python
import anthropic
import base64

client = anthropic.Anthropic()

# Definir las herramientas de computer use
tools = [
    {
        "type": "computer_20251124",  # Version con enhanced actions
        "name": "computer",
        "display_width_px": 1024,
        "display_height_px": 768,
        "display_number": 1,
        "enable_zoom": True,  # Permite inspeccionar regiones especificas
    },
    {
        "type": "bash_20241022",
        "name": "bash",
    },
    {
        "type": "text_editor_20241022",
        "name": "str_replace_editor",
    },
]

# Iniciar la conversacion
response = client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    betas=["computer-use-2025-11-24"],
    tools=tools,
    messages=[{
        "role": "user",
        "content": "Open the terminal and create a new file called test.py with a hello world script"
    }]
)
```

### Loop de Ejecucion

Computer Use funciona en un loop donde Claude pide acciones y tu las ejecutas:

```python
import subprocess
import pyautogui  # Para mouse/keyboard
from PIL import ImageGrab  # Para screenshots

def take_screenshot():
    """Captura la pantalla y retorna base64."""
    img = ImageGrab.grab()
    img = img.resize((1024, 768))
    import io
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.standard_b64encode(buffer.getvalue()).decode()

def execute_computer_action(action):
    """Ejecuta una accion de computer use."""
    action_type = action.get("action")
    
    if action_type == "screenshot":
        return take_screenshot()
    
    elif action_type == "mouse_move":
        x, y = action["coordinate"]
        pyautogui.moveTo(x, y)
    
    elif action_type == "left_click":
        x, y = action["coordinate"]
        pyautogui.click(x, y)
    
    elif action_type == "double_click":
        x, y = action["coordinate"]
        pyautogui.doubleClick(x, y)
    
    elif action_type == "right_click":
        x, y = action["coordinate"]
        pyautogui.rightClick(x, y)
    
    elif action_type == "type":
        pyautogui.write(action["text"], interval=0.02)
    
    elif action_type == "key":
        pyautogui.hotkey(*action["text"].split("+"))
    
    elif action_type == "scroll":
        x, y = action["coordinate"]
        pyautogui.scroll(action["delta_y"], x=x, y=y)
    
    elif action_type == "zoom":
        # Captura region especifica para inspeccion detallada
        region = action["region"]
        # Crop screenshot to region coordinates
        pass
    
    return take_screenshot()

def execute_bash(command):
    """Ejecuta un comando bash."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
    return result.stdout + result.stderr

def run_computer_use_loop(initial_prompt):
    """Loop principal de computer use."""
    messages = [{"role": "user", "content": initial_prompt}]
    
    while True:
        response = client.beta.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            betas=["computer-use-2025-11-24"],
            tools=tools,
            messages=messages,
        )
        
        # Verificar si Claude termino
        if response.stop_reason == "end_turn":
            # Extraer texto final
            for block in response.content:
                if hasattr(block, "text"):
                    print(f"Claude: {block.text}")
            break
        
        # Procesar tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                if block.name == "computer":
                    result = execute_computer_action(block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": [
                            {"type": "image", "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": result
                            }}
                        ]
                    })
                elif block.name == "bash":
                    result = execute_bash(block.input["command"])
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result
                    })
                elif block.name == "str_replace_editor":
                    # Handle text editor actions
                    pass
        
        # Agregar respuesta de Claude y resultados al historial
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
```

### Entorno Seguro con Docker

**IMPORTANTE**: Nunca ejecutar Computer Use en tu maquina principal. Usar Docker:

```dockerfile
# Dockerfile para Computer Use sandbox
FROM ubuntu:22.04

# Desktop environment
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    fluxbox \
    xterm \
    python3 \
    python3-pip \
    firefox \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
RUN pip3 install anthropic pyautogui pillow

# Virtual display
ENV DISPLAY=:1
ENV RESOLUTION=1024x768x24

# Startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 5900 6080

CMD ["/start.sh"]
```

```bash
# start.sh
#!/bin/bash
Xvfb :1 -screen 0 $RESOLUTION &
sleep 1
fluxbox &
x11vnc -display :1 -forever -nopw &
python3 /app/computer_use_agent.py
```

```bash
# Ejecutar
docker build -t computer-use-sandbox .
docker run -p 5900:5900 -p 6080:6080 computer-use-sandbox

# Conectar via VNC para ver que hace Claude
# VNC: localhost:5900
```

### Use Cases Validos (2026)

| Use Case | Viabilidad | Alternativa mejor |
|----------|-----------|-------------------|
| Testing E2E de apps web | Media | Playwright (mas rapido, mas confiable) |
| RPA en apps legacy sin API | Alta | Unica opcion si no hay API |
| Scraping de sitios protegidos | Media | Firecrawl o Playwright CLI |
| Demo automation (videos) | Alta | Bueno para generar demos |
| Form filling automatico | Media | n8n + API directa si existe |
| Data entry en ERPs legacy | Alta | Ideal — no hay API en ERPs viejos |
| Monitoreo visual de dashboards | Baja | Better con APIs + alertas |

### Computer Use vs n8n para RPA

**Decision Record (ADR-003):**

| Factor | Computer Use | n8n |
|--------|-------------|-----|
| Madurez | Beta | Produccion |
| Velocidad | 2-5s por accion | Milisegundos por nodo |
| Confiabilidad | ~85% accuracy | ~99% con nodos nativos |
| Costo | Alto (vision tokens) | Bajo (ejecucion simple) |
| Flexibilidad | Cualquier UI | Solo APIs y webhooks |
| Mantenimiento | Alto (UI cambia) | Bajo (APIs estables) |
| Escalabilidad | 1 tarea a la vez | Miles concurrentes |

**Recomendacion:**
- **Usar n8n** para todo lo que tenga API (95% de los casos)
- **Usar Computer Use** solo para apps legacy sin API o testing visual
- **Re-evaluar** en Q3 2026 cuando Computer Use salga de beta

### Limitaciones Actuales

1. **Latencia**: 2-5 segundos por accion. Un flujo de 20 acciones toma ~1 minuto.
2. **Accuracy**: ~85% en tareas simples. Baja con UIs complejas o elementos pequenos.
3. **Costo**: Cada screenshot es una imagen en la API (~$0.005-0.01 por screenshot con Sonnet).
4. **Sesion**: No persiste estado entre llamadas API. Debes manejar el loop tu mismo.
5. **Seguridad**: Claude tiene control total del mouse/teclado. Sandbox obligatorio.
6. **Windows**: Soporte limitado. Linux es la plataforma recomendada.
7. **Resoluciones altas**: Mejor rendimiento con 1024x768. 4K causa problemas.

### Roadmap Esperado

| Timeline | Milestone esperado |
|----------|-------------------|
| Q2 2026 | Mejoras en accuracy y velocidad (Anthropic activo) |
| Q3 2026 | Posible soporte nativo Windows |
| Q4 2026 | GA (General Availability) estimado |
| Q1 2027 | Windows production support + enterprise features |

**Decision gate para la Agencia:**
- **Ahora**: Research only. Spike de 40h para entender capacidades.
- **Q3 2026**: Re-evaluar con landscape actualizado.
- **Q4 2026+**: Adoptar si GA y Windows support confirmado.

### Benchmark Template

Para el spike de Sasha, medir estos puntos:

```markdown
## Computer Use Benchmark Report

### Test 1: Abrir VS Code y crear archivo
- Tiempo total: ___ segundos
- Acciones ejecutadas: ___
- Resultado: PASS / FAIL
- Errores: ___

### Test 2: Navegar un sitio web y extraer datos
- Tiempo total: ___ segundos
- Datos extraidos correctamente: ___/___
- Resultado: PASS / FAIL

### Test 3: Llenar formulario web
- Tiempo total: ___ segundos
- Campos llenados correctamente: ___/___
- Resultado: PASS / FAIL

### Test 4: Interactuar con app de escritorio
- Tiempo total: ___ segundos
- Acciones completadas: ___/___
- Resultado: PASS / FAIL

### Resumen
- Accuracy promedio: ___%
- Latencia promedio por accion: ___ ms
- Costo promedio por tarea: $___
- Readiness score (1-10): ___
- Recomendacion: ADOPTAR / ESPERAR / DESCARTAR
```

### Mejores Practicas

1. **Siempre usar Docker/VM**: Nunca en maquina principal. Claude tiene control total.
2. **Screenshots a 1024x768**: Mejor accuracy que resoluciones altas.
3. **Prompts especificos**: "Click the blue Submit button at the bottom of the form" es mejor que "Submit the form".
4. **Timeouts**: Configurar timeout de 30s por accion para evitar loops infinitos.
5. **Logging**: Guardar cada screenshot y accion para debugging post-mortem.
6. **Fallback manual**: Siempre tener un plan B si Computer Use falla a mitad de tarea.
7. **No para datos sensibles**: No usar Computer Use para login en bancos, credenciales, etc.
