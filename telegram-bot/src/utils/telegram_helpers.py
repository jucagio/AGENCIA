MAX_MESSAGE_LEN = 4000  # margen de seguridad bajo el limite de 4096 de Telegram


def split_long_text(text: str) -> list[str]:
    """Divide texto en chunks de maximo MAX_MESSAGE_LEN chars."""
    if len(text) <= MAX_MESSAGE_LEN:
        return [text]
    chunks = []
    while text:
        chunks.append(text[:MAX_MESSAGE_LEN])
        text = text[MAX_MESSAGE_LEN:]
    return chunks
