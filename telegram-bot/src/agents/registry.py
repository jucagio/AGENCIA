from dataclasses import dataclass
from pathlib import Path

_PROMPTS_DIR = Path(__file__).parent / "prompts"


@dataclass(frozen=True)
class AgentConfig:
    name: str
    model: str
    display_name: str
    emoji: str


AGENT_REGISTRY: dict[str, AgentConfig] = {
    "jarvis":  AgentConfig("jarvis",  "claude-opus-4-5",    "Jarvis",  "\U0001f916"),
    "jade":    AgentConfig("jade",    "claude-sonnet-4-5",  "Jade",    "\U0001f52e"),
    "sasha":   AgentConfig("sasha",   "claude-opus-4-5",    "Sasha",   "\U0001f4bb"),
    "brook":   AgentConfig("brook",   "claude-sonnet-4-5",  "Brook",   "\U0001f30a"),
    "erik":    AgentConfig("erik",    "claude-sonnet-4-5",  "Erik",    "\U0001f3a8"),
    "cinthya": AgentConfig("cinthya", "claude-sonnet-4-5",  "Cinthya", "\u2699\ufe0f"),
    "ego":     AgentConfig("ego",     "claude-opus-4-5",    "Ego",     "\U0001f441"),
}


def get_agent(mention: str) -> AgentConfig | None:
    key = mention.lstrip("@").lower()
    return AGENT_REGISTRY.get(key)


def load_system_prompt(agent_name: str) -> str:
    path = _PROMPTS_DIR / f"{agent_name}.txt"
    if not path.exists():
        raise FileNotFoundError(
            f"System prompt no encontrado: {path}. "
            f"Crea el archivo prompts/{agent_name}.txt."
        )
    return path.read_text(encoding="utf-8")
