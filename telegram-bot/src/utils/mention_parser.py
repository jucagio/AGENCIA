import re
from dataclasses import dataclass

AGENT_NAMES = ["jarvis", "jade", "sasha", "brook", "erik", "cinthya", "ego"]
_PATTERN = re.compile(
    r"@(" + "|".join(AGENT_NAMES) + r")\b",
    re.IGNORECASE,
)


@dataclass
class ParsedMessage:
    agent_name: str | None
    content: str
    has_ultrathink: bool


def parse_message(text: str) -> ParsedMessage:
    match = _PATTERN.search(text)
    agent_name = match.group(1).lower() if match else None
    content = _PATTERN.sub("", text).strip() if match else text.strip()
    has_ultrathink = "ultrathink" in text.lower()
    return ParsedMessage(agent_name=agent_name, content=content, has_ultrathink=has_ultrathink)
