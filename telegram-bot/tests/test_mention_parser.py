from src.utils.mention_parser import parse_message


def test_basic_mention():
    result = parse_message("@jarvis evalua este proyecto")
    assert result.agent_name == "jarvis"
    assert result.content == "evalua este proyecto"
    assert not result.has_ultrathink


def test_ultrathink_flag():
    result = parse_message("@jade dame tendencias. Ultrathink")
    assert result.agent_name == "jade"
    assert result.has_ultrathink


def test_no_mention():
    result = parse_message("hola, como estas?")
    assert result.agent_name is None
    assert result.content == "hola, como estas?"


def test_case_insensitive():
    result = parse_message("@SASHA revisa este codigo")
    assert result.agent_name == "sasha"


def test_unknown_agent_returns_none_name():
    result = parse_message("@desconocido haz algo")
    assert result.agent_name is None
    assert "@desconocido haz algo" in result.content


def test_content_stripped():
    result = parse_message("  @brook   construye el dashboard  ")
    assert result.agent_name == "brook"
    assert result.content == "construye el dashboard"
